# -*- coding: utf-8 -*-
# openpgp.py
# Copyright (C) 2013-2017 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Infrastructure for using OpenPGP keys in Key Manager.
"""

import os
import re
import tempfile
import traceback
import io


from datetime import datetime
from multiprocessing import cpu_count
from twisted.internet import defer
from twisted.internet.threads import deferToThread
from twisted.logger import Logger

from leap.common.check import leap_assert, leap_assert_type, leap_check
from leap.bitmask.keymanager import errors
from leap.bitmask.keymanager.wrapper import TempGPGWrapper
from leap.bitmask.keymanager.keys import (
    OpenPGPKey,
    is_address,
    parse_address,
    build_key_from_dict,
)
from leap.bitmask.keymanager.documents import (
    init_indexes,
    TAGS_PRIVATE_INDEX,
    TYPE_FINGERPRINT_PRIVATE_INDEX,
    TYPE_ADDRESS_PRIVATE_INDEX,
    KEY_UIDS_KEY,
    KEY_FINGERPRINT_KEY,
    KEY_PRIVATE_KEY,
    KEY_REFRESHED_AT_KEY,
    KEY_SIGN_USED_KEY,
    KEY_ENCR_USED_KEY,
    KEY_ADDRESS_KEY,
    KEY_TYPE_KEY,
    KEY_VERSION_KEY,
    KEYMANAGER_DOC_VERSION,
    KEYMANAGER_ACTIVE_TYPE,
    KEYMANAGER_KEY_TAG,
    KEYMANAGER_ACTIVE_TAG,
)
try:
    from gnupg.gnupg import GPGUtilities
    GNUPG_NG = True
except ImportError:
    GNUPG_NG = False

    class GPGUtilities(object):

        def __init__(self, gpg):
            self.gpg = gpg

        def is_encrypted_asym(self, raw_data):
            result = self._gpg.list_packets(raw_data)
            return bool(result.key)


# This function will be used to call blocking GPG functions outside
# of Twisted reactor and match the concurrent calls to the amount of CPU cores
cpu_core_semaphore = defer.DeferredSemaphore(cpu_count())


def from_thread(func, *args, **kwargs):
    call = lambda: deferToThread(func, *args, **kwargs)
    return cpu_core_semaphore.run(call)


log = Logger()


#
# The OpenPGP wrapper
#

class OpenPGPScheme(object):

    """
    A wrapper for OpenPGP keys management and use (encryption, decyption,
    signing and verification).
    """

    log = Logger()

    # type used on the soledad documents
    KEY_TYPE = OpenPGPKey.__name__
    ACTIVE_TYPE = KEY_TYPE + KEYMANAGER_ACTIVE_TYPE

    def __init__(self, soledad, gpgbinary=None):
        """
        Initialize the OpenPGP wrapper.

        :param soledad: A Soledad instance for key storage.
        :type soledad: leap.soledad.Soledad
        :param gpgbinary: Name for GnuPG binary executable.
        :type gpgbinary: C{str}
        """
        self._soledad = soledad
        self._gpgbinary = gpgbinary
        self.deferred_init = init_indexes(soledad)
        self.deferred_init.addCallback(self._migrate_documents_schema)
        self._wait_indexes("get_key", "put_key", "get_all_keys")

    def _migrate_documents_schema(self, _):
        from leap.bitmask.keymanager.migrator import KeyDocumentsMigrator
        migrator = KeyDocumentsMigrator(self._soledad)
        return migrator.migrate()

    def _wait_indexes(self, *methods):
        """
        Methods that need to wait for the indexes to be ready.

        Heavily based on
        http://blogs.fluidinfo.com/terry/2009/05/11/a-mixin-class-allowing-python-__init__-methods-to-work-with-twisted-deferreds/

        :param methods: methods that need to wait for the indexes to be ready
        :type methods: tuple(str)
        """
        self.waiting = []
        self.stored = {}

        def restore(_):
            for method in self.stored:
                setattr(self, method, self.stored[method])
            for d in self.waiting:
                d.callback(None)

        def makeWrapper(method):
            def wrapper(*args, **kw):
                d = defer.Deferred()
                d.addCallback(lambda _: self.stored[method](*args, **kw))
                self.waiting.append(d)
                return d
            return wrapper

        for method in methods:
            self.stored[method] = getattr(self, method)
            setattr(self, method, makeWrapper(method))

        self.deferred_init.addCallback(restore)

    #
    # Keys management
    #

    def gen_key(self, address):
        """
        Generate an OpenPGP keypair bound to C{address}.

        :param address: The address bound to the key.
        :type address: str

        :return: A Deferred which fires with the key bound to address, or fails
                 with KeyAlreadyExists if key already exists in local database.
        :rtype: Deferred
        """
        # make sure the key does not already exist
        leap_assert(is_address(address), 'Not an user address: %s' % address)

        @defer.inlineCallbacks
        def _gen_key(_):
            with TempGPGWrapper(gpgbinary=self._gpgbinary) as gpg:
                # TODO: inspect result, or use decorator
                params = gpg.gen_key_input(
                    key_type='RSA',
                    key_length=4096,
                    name_real=address,
                    name_email=address,
                    name_comment='')
                self.log.info('About to generate keys... '
                              'This might take SOME time.')
                yield from_thread(gpg.gen_key, params)
                self.log.info('Keys for %s have been successfully '
                              'generated.' % (address,))
                pubkeys = gpg.list_keys()

                # assert for new key characteristics
                leap_assert(
                    len(pubkeys) is 1,  # a unitary keyring!
                    'Keyring has wrong number of keys: %d.' % len(pubkeys))
                key = gpg.list_keys(secret=True).pop()
                leap_assert(
                    len(key['uids']) is 1,  # with just one uid!
                    'Wrong number of uids for key: %d.' % len(key['uids']))
                uid_match = False
                for uid in key['uids']:
                    if re.match('.*<%s>$' % address, uid) is not None:
                        uid_match = True
                        break
                leap_assert(uid_match, 'Key not correctly bound to address.')

                # insert both public and private keys in storage
                deferreds = []
                for secret in [True, False]:
                    key = gpg.list_keys(secret=secret).pop()
                    openpgp_key = self._build_key_from_gpg(
                        key,
                        gpg.export_keys(key['fingerprint'], secret=secret),
                        address)
                    d = self.put_key(openpgp_key)
                    deferreds.append(d)
                yield defer.gatherResults(deferreds)

        def key_already_exists(_):
            raise errors.KeyAlreadyExists(address)

        d = self.get_key(address)
        d.addCallbacks(key_already_exists, _gen_key)
        d.addCallback(lambda _: self.get_key(address, private=False))
        return d

    def get_key(self, address, private=False):
        """
        Get key bound to C{address} from local storage.

        :param address: The address bound to the key.
        :type address: str
        :param private: Look for a private key instead of a public one?
        :type private: bool

        :return: A Deferred which fires with the OpenPGPKey bound to address,
                 or which fails with KeyNotFound if the key was not found on
                 local storage.
        :rtype: Deferred
        """
        address = parse_address(address)

        def build_key((keydoc, activedoc)):
            if keydoc is None:
                raise errors.KeyNotFound(address)
            leap_assert(
                address in keydoc.content[KEY_UIDS_KEY],
                'Wrong address in key %s. Expected %s, found %s.'
                % (keydoc.content[KEY_FINGERPRINT_KEY], address,
                   keydoc.content[KEY_UIDS_KEY]))
            key = build_key_from_dict(keydoc.content, activedoc.content)
            key._gpgbinary = self._gpgbinary
            return key

        d = self._get_key_doc(address, private)
        d.addCallback(build_key)
        return d

    @defer.inlineCallbacks
    def get_all_keys(self, private=False):
        """
        Return all keys stored in local database.

        :param private: Include private keys
        :type private: bool

        :return: A Deferred which fires with a list of all keys in local db.
        :rtype: Deferred
        """
        HAS_ACTIVE = "has_active"

        active_docs = yield self._soledad.get_from_index(
            TAGS_PRIVATE_INDEX,
            KEYMANAGER_ACTIVE_TAG,
            '1' if private else '0')
        key_docs = yield self._soledad.get_from_index(
            TAGS_PRIVATE_INDEX,
            KEYMANAGER_KEY_TAG,
            '1' if private else '0')

        keys = []
        fp = lambda doc: doc.content[KEY_FINGERPRINT_KEY]
        for active in active_docs:
            fp_keys = filter(lambda k: fp(k) == fp(active), key_docs)

            if len(fp_keys) == 0:
                yield self._soledad.delete_doc(active)
                continue
            elif len(fp_keys) == 1:
                key = fp_keys[0]
            else:
                key = yield self._repair_key_docs(fp_keys)
            key.content[HAS_ACTIVE] = True
            keys.append(build_key_from_dict(key.content, active.content))

        unactive_keys = filter(lambda k: HAS_ACTIVE not in k.content, key_docs)
        keys += map(lambda k: build_key_from_dict(k.content), unactive_keys)
        defer.returnValue(keys)

    def parse_key(self, key_data, address=None):
        """
        Parses a key (or key pair) data and returns
        the OpenPGPKey keys.

        :param key_data: the key data to be parsed.
        :type key_data: str or unicode
        :param address: Active address for the key.
        :type address: str

        :returns: the public key and private key (if applies) for that data.
        :rtype: (public, private) -> tuple(OpenPGPKey, OpenPGPKey)
                the tuple may have one or both components None
        """
        leap_assert_type(key_data, (str, unicode))
        # TODO: add more checks for correct key data.
        leap_assert(key_data is not None, 'Data does not represent a key.')

        priv_info, privkey = process_key(
            key_data, self._gpgbinary, secret=True)
        pub_info, pubkey = process_key(
            key_data, self._gpgbinary, secret=False)

        if not pubkey:
            return (None, None)

        openpgp_privkey = None
        if privkey:
            # build private key
            openpgp_privkey = self._build_key_from_gpg(priv_info, privkey,
                                                       address)
            leap_check(pub_info['fingerprint'] == priv_info['fingerprint'],
                       'Fingerprints for public and private key differ.',
                       errors.KeyFingerprintMismatch)
        # build public key
        openpgp_pubkey = self._build_key_from_gpg(pub_info, pubkey, address)

        return (openpgp_pubkey, openpgp_privkey)

    def put_raw_key(self, key_data, address):
        """
        Put key contained in C{key_data} in local storage.

        :param key_data: The key data to be stored.
        :type key_data: str or unicode
        :param address: address for which this key will be active
        :type address: str

        :return: A Deferred which fires when the OpenPGPKey is in the storage.
        :rtype: Deferred
        """
        leap_assert_type(key_data, (str, unicode))

        openpgp_privkey = None
        try:
            openpgp_pubkey, openpgp_privkey = self.parse_key(
                key_data, address)
        except (errors.KeyAddressMismatch, errors.KeyFingerprintMismatch) as e:
            return defer.fail(e)

        def put_key(_, key):
            return self.put_key(key)

        d = defer.succeed(None)
        if openpgp_pubkey is not None:
            d.addCallback(put_key, openpgp_pubkey)
        if openpgp_privkey is not None:
            d.addCallback(put_key, openpgp_privkey)
        return d

    def put_key(self, key):
        """
        Put C{key} in local storage.

        :param key: The key to be stored.
        :type key: OpenPGPKey

        :return: A Deferred which fires when the key is in the storage.
        :rtype: Deferred
        """
        def merge_and_put((keydoc, activedoc)):
            if not keydoc:
                return put_new_key(activedoc)

            active_content = None
            if activedoc:
                active_content = activedoc.content
            oldkey = build_key_from_dict(keydoc.content, active_content)

            key.merge(oldkey)
            keydoc.set_json(key.get_json())
            d = self._soledad.put_doc(keydoc)
            d.addCallback(put_active, activedoc)
            return d

        def put_new_key(activedoc):
            deferreds = []
            if activedoc:
                d = self._soledad.delete_doc(activedoc)
                deferreds.append(d)
            for json in [key.get_json(), key.get_active_json()]:
                d = self._soledad.create_doc_from_json(json)
                deferreds.append(d)
            return defer.gatherResults(deferreds)

        def put_active(_, activedoc):
            active_json = key.get_active_json()
            if activedoc:
                activedoc.set_json(active_json)
                return self._soledad.put_doc(activedoc)
            elif key.is_active():
                return self._soledad.create_doc_from_json(active_json)

        def get_active_doc(keydoc):
            d = self._get_active_doc_from_address(key.address, key.private)
            d.addCallback(lambda activedoc: (keydoc, activedoc))
            return d

        d = self._get_key_doc_from_fingerprint(key.fingerprint, key.private)
        d.addCallback(get_active_doc)
        d.addCallback(merge_and_put)
        return d

    def _get_key_doc(self, address, private=False):
        """
        Get the document with a key (public, by default) bound to C{address}.

        If C{private} is True, looks for a private key instead of a public.

        :param address: The address bound to the key.
        :type address: str
        :param private: Whether to look for a private key.
        :type private: bool

        :return: A Deferred which fires with a touple of two SoledadDocument
                 (keydoc, activedoc) or None if it does not exist.
        :rtype: Deferred
        """
        def get_key_from_active_doc(activedoc):
            if not activedoc:
                return (None, None)
            fingerprint = activedoc.content[KEY_FINGERPRINT_KEY]
            d = self._get_key_doc_from_fingerprint(fingerprint, private)
            d.addCallback(delete_active_if_no_key, activedoc)
            return d

        def delete_active_if_no_key(keydoc, activedoc):
            if not keydoc:
                d = self._soledad.delete_doc(activedoc)
                d.addCallback(lambda _: (None, None))
                return d
            return (keydoc, activedoc)

        d = self._get_active_doc_from_address(address, private)
        d.addCallback(get_key_from_active_doc)
        return d

    def _build_key_from_gpg(self, key, key_data, address=None):
        """
        Build an OpenPGPKey for C{address} based on C{key} from
        local gpg storage.

        GPG key data has to be queried independently in this
        wrapper, so we receive it in C{key_data}.

        :param address: Active address for the key.
        :type address: str
        :param key: Key obtained from GPG storage.
        :type key: dict
        :param key_data: Key data obtained from GPG storage.
        :type key_data: str
        :return: An instance of the key.
        :rtype: OpenPGPKey
        """
        return build_gpg_key(key, key_data, address, self._gpgbinary)

    def delete_key(self, key):
        """
        Remove C{key} from storage.

        :param key: The key to be removed.
        :type key: EncryptionKey

        :return: A Deferred which fires when the key is deleted, or which
                 fails with KeyNotFound if the key was not found on local
                 storage.
        :rtype: Deferred
        """
        leap_assert_type(key, OpenPGPKey)

        def delete_docs(activedocs):
            deferreds = []
            for doc in activedocs:
                d = self._soledad.delete_doc(doc)
                deferreds.append(d)
            return defer.gatherResults(deferreds)

        def get_key_docs(_):
            return self._soledad.get_from_index(
                TYPE_FINGERPRINT_PRIVATE_INDEX,
                self.KEY_TYPE,
                key.fingerprint,
                '1' if key.private else '0')

        def delete_key(docs):
            if len(docs) == 0:
                raise errors.KeyNotFound(key)
            elif len(docs) > 1:
                self.log.warn('There is more than one key for fingerprint %s'
                              % key.fingerprint)

            has_deleted = False
            deferreds = []
            for doc in docs:
                if doc.content['fingerprint'] == key.fingerprint:
                    d = self._soledad.delete_doc(doc)
                    deferreds.append(d)
                    has_deleted = True
            if not has_deleted:
                raise errors.KeyNotFound(key)
            return defer.gatherResults(deferreds)

        d = self._soledad.get_from_index(
            TYPE_FINGERPRINT_PRIVATE_INDEX,
            self.ACTIVE_TYPE,
            key.fingerprint,
            '1' if key.private else '0')
        d.addCallback(delete_docs)
        d.addCallback(get_key_docs)
        d.addCallback(delete_key)
        return d

    @defer.inlineCallbacks
    def unactivate_key(self, address):
        """
        Mark a active doc as deleted.
        :param address: The unique address for the active content.
        """
        active_doc = yield self._get_active_doc_from_address(address, False)
        yield self._soledad.delete_doc(active_doc)

    #
    # Data encryption, decryption, signing and verifying
    #

    @staticmethod
    def _assert_gpg_result_ok(result):
        """
        Check if GPG result is 'ok' and log stderr outputs.

        :param result: GPG results, which have a field calld 'ok' that states
                       whether the gpg operation was successful or not.
        :type result: object

        :raise GPGError: Raised when the gpg operation was not successful.
        """
        stderr = getattr(result, 'stderr', None)
        if stderr:
            log.debug("%s" % (stderr,))
        if getattr(result, 'ok', None) is not True:
            raise errors.GPGError(
                'Failed to encrypt/decrypt: %s' % stderr)

    @defer.inlineCallbacks
    def encrypt(self, data, pubkey, passphrase=None, sign=None,
                cipher_algo='AES256'):
        """
        Encrypt C{data} using public @{pubkey} and sign with C{sign} key.

        :param data: The data to be encrypted.
        :type data: str
        :param pubkey: The key used to encrypt.
        :type pubkey: OpenPGPKey
        :param sign: The key used for signing.
        :type sign: OpenPGPKey
        :param cipher_algo: The cipher algorithm to use.
        :type cipher_algo: str

        :return: A Deferred that will be fired with the encrypted data.
        :rtype: defer.Deferred

        :raise EncryptError: Raised if failed encrypting for some reason.
        """
        leap_assert_type(pubkey, OpenPGPKey)
        leap_assert(pubkey.private is False, 'Key is not public.')
        keys = [pubkey]
        if sign is not None:
            leap_assert_type(sign, OpenPGPKey)
            leap_assert(sign.private is True)
            keys.append(sign)
        with TempGPGWrapper(keys, self._gpgbinary) as gpg:
            kw = dict(
                default_key=sign.fingerprint if sign else None,
                passphrase=passphrase, symmetric=False,
                cipher_algo=cipher_algo)
            if not GNUPG_NG:
                kw.pop('cipher_algo')
                kw.pop('default_key')
                kw.update(passphrase='')
                kw.update(always_trust=True)
            result = yield from_thread(
                gpg.encrypt,
                data, pubkey.fingerprint, **kw)
            # Here we cannot assert for correctness of sig because the sig is
            # in the ciphertext.
            # result.ok    - (bool) indicates if the operation succeeded
            # result.data  - (bool) contains the result of the operation
            try:
                self._assert_gpg_result_ok(result)
                defer.returnValue(result.data)
            except errors.GPGError as e:
                self.log.warn('Failed to encrypt: %s.' % str(e))
                raise errors.EncryptError()

    @defer.inlineCallbacks
    def decrypt(self, data, privkey, passphrase=None, verify=None):
        """
        Decrypt C{data} using private @{privkey} and verify with C{verify} key.

        :param data: The data to be decrypted.
        :type data: str
        :param privkey: The key used to decrypt.
        :type privkey: OpenPGPKey
        :param passphrase: The passphrase for the secret key used for
                           decryption.
        :type passphrase: str
        :param verify: The key used to verify a signature.
        :type verify: OpenPGPKey

        :return: Deferred that will fire with the decrypted data and
                 if signature verifies (unicode, bool)
        :rtype: Deferred

        :raise DecryptError: Raised if failed decrypting for some reason.
        """
        leap_assert(privkey.private is True, 'Key is not private.')
        keys = [privkey]
        if verify is not None:
            leap_assert_type(verify, OpenPGPKey)
            leap_assert(verify.private is False)
            keys.append(verify)
        with TempGPGWrapper(keys, self._gpgbinary) as gpg:
            try:
                result = yield from_thread(gpg.decrypt,
                                           data, passphrase=passphrase,
                                           always_trust=True)
                self._assert_gpg_result_ok(result)

                # verify signature
                sign_valid = False
                if (verify is not None and
                        result.valid is True and
                        verify.fingerprint == result.pubkey_fingerprint):
                    sign_valid = True

                defer.returnValue((result.data, sign_valid))
            except errors.GPGError as e:
                self.log.warn('Failed to decrypt: %s.' % str(e))
                raise errors.DecryptError(str(e))

    def is_encrypted(self, data):
        """
        Return whether C{data} was asymmetrically encrypted using OpenPGP.

        :param data: The data we want to know about.
        :type data: str

        :return: Whether C{data} was encrypted using this wrapper.
        :rtype: bool
        """
        with TempGPGWrapper(gpgbinary=self._gpgbinary) as gpg:
            gpgutil = GPGUtilities(gpg)
            return gpgutil.is_encrypted_asym(data)

    def sign(self, data, privkey, digest_algo='SHA512', clearsign=False,
             detach=True, binary=False):
        """
        Sign C{data} with C{privkey}.

        :param data: The data to be signed.
        :type data: str

        :param privkey: The private key to be used to sign.
        :type privkey: OpenPGPKey
        :param digest_algo: The hash digest to use.
        :type digest_algo: str
        :param clearsign: If True, create a cleartext signature.
        :type clearsign: bool
        :param detach: If True, create a detached signature.
        :type detach: bool
        :param binary: If True, do not ascii armour the output.
        :type binary: bool

        :return: The ascii-armored signed data.
        :rtype: str
        """
        leap_assert_type(privkey, OpenPGPKey)
        leap_assert(privkey.private is True)

        # result.fingerprint - contains the fingerprint of the key used to
        #                      sign.
        with TempGPGWrapper(privkey, self._gpgbinary) as gpg:
            kw = dict(default_key=privkey.fingerprint,
                      digest_algo=digest_algo, clearsign=clearsign,
                      detach=detach, binary=binary)
            if not GNUPG_NG:
                kw.pop('digest_algo')
                kw.pop('default_key')
            result = gpg.sign(data, **kw)
            rfprint = privkey.fingerprint
            privkey = gpg.list_keys(secret=True).pop()
            kfprint = privkey['fingerprint']
            if result.fingerprint is None:
                raise errors.SignFailed(
                    'Failed to sign with key %s: %s' %
                    (privkey['fingerprint'], result.stderr))
            leap_assert(
                result.fingerprint == kfprint,
                'Signature and private key fingerprints mismatch: '
                '%s != %s' % (rfprint, kfprint))
        return result.data

    def verify(self, data, pubkey, detached_sig=None):
        """
        Verify signed C{data} with C{pubkey}, eventually using
        C{detached_sig}.

        :param data: The data to be verified.
        :type data: str
        :param pubkey: The public key to be used on verification.
        :type pubkey: OpenPGPKey
        :param detached_sig: A detached signature. If given, C{data} is
                             verified against this detached signature.
        :type detached_sig: str

        :return: signature matches
        :rtype: bool
        """
        leap_assert_type(pubkey, OpenPGPKey)
        leap_assert(pubkey.private is False)
        with TempGPGWrapper(pubkey, self._gpgbinary) as gpg:
            result = None
            if detached_sig is None:
                result = gpg.verify(data)
            else:
                # to verify using a detached sig we have to use
                # gpg.verify_file(), which receives the data as a binary
                # stream and the name of a file containing the signature.
                sf, sfname = tempfile.mkstemp()
                with os.fdopen(sf, 'w') as sfd:
                    sfd.write(detached_sig)
                result = gpg.verify_file(io.BytesIO(data), sig_file=sfname)
                os.unlink(sfname)
            gpgpubkey = gpg.list_keys().pop()
            valid = result.valid
            rfprint = result.fingerprint
            kfprint = gpgpubkey['fingerprint']
            return valid and rfprint == kfprint

    def _get_active_doc_from_address(self, address, private):
        d = self._soledad.get_from_index(
            TYPE_ADDRESS_PRIVATE_INDEX,
            self.ACTIVE_TYPE,
            address,
            '1' if private else '0')
        d.addCallback(self._repair_and_get_doc, self._repair_active_docs)
        d.addCallback(self._check_version)
        return d

    def _get_key_doc_from_fingerprint(self, fingerprint, private):
        d = self._soledad.get_from_index(
            TYPE_FINGERPRINT_PRIVATE_INDEX,
            self.KEY_TYPE,
            fingerprint,
            '1' if private else '0')
        d.addCallback(self._repair_and_get_doc, self._repair_key_docs)
        d.addCallback(self._check_version)
        return d

    def _repair_and_get_doc(self, doclist, repair_func):
        if len(doclist) is 0:
            return None
        elif len(doclist) > 1:
            return repair_func(doclist)
        return doclist[0]

    def _check_version(self, doc):
        if doc is not None:
            version = doc.content[KEY_VERSION_KEY]
            if version > KEYMANAGER_DOC_VERSION:
                raise errors.KeyVersionError(str(version))
        return doc

    def _repair_key_docs(self, doclist):
        """
        If there is more than one key for a key id try to self-repair it

        :return: a Deferred that will be fired with the valid key doc once all
                 the deletions are completed
        :rtype: Deferred
        """
        def log_key_doc(doc):
            self.log.error("\t%s: %s" % (doc.content[KEY_UIDS_KEY],
                                         doc.content[KEY_FINGERPRINT_KEY]))

        def cmp_key(d1, d2):
            return cmp(d1.content[KEY_REFRESHED_AT_KEY],
                       d2.content[KEY_REFRESHED_AT_KEY])

        return self._repair_docs(doclist, cmp_key, log_key_doc)

    @defer.inlineCallbacks
    def _repair_active_docs(self, doclist):
        """
        If there is more than one active doc for an address try to self-repair
        it

        :return: a Deferred that will be fired with the valid active doc once
                 all the deletions are completed
        :rtype: Deferred
        """
        keys = {}
        for doc in doclist:
            fp = doc.content[KEY_FINGERPRINT_KEY]
            private = doc.content[KEY_PRIVATE_KEY]
            try:
                key = yield self._get_key_doc_from_fingerprint(fp, private)
                keys[fp] = key
            except Exception:
                pass

        def log_active_doc(doc):
            self.log.error("\t%s: %s" % (doc.content[KEY_ADDRESS_KEY],
                                         doc.content[KEY_FINGERPRINT_KEY]))

        def cmp_active(d1, d2):
            # XXX: for private keys it will be nice to check which key is known
            #      by the nicknym server and keep this one. But this needs a
            #      refactor that might not be worth it.
            used1 = (d1.content[KEY_SIGN_USED_KEY] +
                     d1.content[KEY_ENCR_USED_KEY])
            used2 = (d2.content[KEY_SIGN_USED_KEY] +
                     d2.content[KEY_ENCR_USED_KEY])
            res = cmp(used1, used2)
            if res != 0:
                return res

            key1 = keys[d1.content[KEY_FINGERPRINT_KEY]]
            key2 = keys[d2.content[KEY_FINGERPRINT_KEY]]
            return cmp(key1.content[KEY_REFRESHED_AT_KEY],
                       key2.content[KEY_REFRESHED_AT_KEY])

        doc = yield self._repair_docs(doclist, cmp_active, log_active_doc)
        defer.returnValue(doc)

    def _repair_docs(self, doclist, cmp_func, log_func):
        self.log.error("BUG -------------------------------------------------")
        self.log.error("There is more than one doc of type %s:"
                       % (doclist[0].content[KEY_TYPE_KEY],))

        doclist.sort(cmp=cmp_func, reverse=True)
        log_func(doclist[0])
        deferreds = []
        for doc in doclist[1:]:
            log_func(doc)
            d = self._soledad.delete_doc(doc)
            deferreds.append(d)

        self.log.error('Error repairing')
        self.log.error("BUG (please report above info) ----------------------")
        d = defer.gatherResults(deferreds, consumeErrors=True)
        d.addCallback(lambda _: doclist[0])
        return d


def process_key(key_data, gpgbinary, secret=False):
    with TempGPGWrapper(gpgbinary=gpgbinary) as gpg:
        try:
            gpg.import_keys(key_data)
            info = gpg.list_keys(secret=secret).pop()
            key = gpg.export_keys(info['fingerprint'], secret=secret)
        except IndexError:
            info = {}
            key = None
    return info, key


def build_gpg_key(key_info, key_data, address=None, gpgbinary=None):
    expiry_date = None
    if key_info['expires']:
        expiry_date = datetime.fromtimestamp(int(key_info['expires']))
    uids = []
    for uid in key_info['uids']:
        uids.append(parse_address(uid))
    if address and address not in uids:
        raise errors.KeyAddressMismatch("UIDs %s found, but expected %s"
                                        % (str(uids), address))

    return OpenPGPKey(
        address=address,
        uids=uids,
        gpgbinary=gpgbinary,
        fingerprint=key_info['fingerprint'],
        key_data=key_data,
        private=True if key_info['type'] == 'sec' else False,
        length=int(key_info['length']),
        expiry_date=expiry_date,
        refreshed_at=datetime.now())
