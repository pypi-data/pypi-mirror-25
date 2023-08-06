# soledad.py
# Copyright (C) 2014 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Soledadad MailAdaptor module.
"""
import re

from collections import defaultdict
from email import message_from_string

from twisted.internet import defer
from twisted.logger import Logger
from zope.interface import implements

from leap.common.check import leap_assert, leap_assert_type

from leap.bitmask.mail import constants
from leap.bitmask.mail import walk
from leap.bitmask.mail.adaptors import soledad_indexes as indexes
from leap.bitmask.mail.constants import INBOX_NAME
from leap.bitmask.mail.adaptors import models
from leap.bitmask.mail.imap.mailbox import normalize_mailbox
from leap.bitmask.mail.utils import lowerdict, first
from leap.bitmask.mail.utils import stringify_parts_map
from leap.bitmask.mail.interfaces import IMailAdaptor, IMessageWrapper

from leap.soledad.common import l2db
from leap.soledad.common.document import SoledadDocument


# TODO
# [ ] Convenience function to create mail specifying subject, date, etc?


_MSGID_PATTERN = r"""<([\w@.]+)>"""
_MSGID_RE = re.compile(_MSGID_PATTERN)


class DuplicatedDocumentError(Exception):
    """
    Raised when a duplicated document is detected.
    """
    pass


def cleanup_deferred_locks():
    """
    Need to use this from within trial to cleanup the reactor before
    each run.
    """
    SoledadDocumentWrapper._k_locks = defaultdict(defer.DeferredLock)


class SoledadDocumentWrapper(models.DocumentWrapper):

    """
    A Wrapper object that can be manipulated, passed around, and serialized in
    a format that the Soledad Store understands.

    It ensures atomicity of the document operations on creation, update and
    deletion.
    """

    log = Logger()

    # TODO we could also use a _dirty flag (in models)
    # TODO add a get_count() method ??? -- that is extended over l2db.

    # We keep a dictionary with DeferredLocks, that will be
    # unique to every subclass of SoledadDocumentWrapper.
    _k_locks = defaultdict(defer.DeferredLock)

    @classmethod
    def _get_klass_lock(cls):
        """
        Get a DeferredLock that is unique for this subclass name.
        Used to lock the access to indexes in the `get_or_create` call
        for a particular DocumentWrapper.
        """
        return cls._k_locks[cls.__name__]

    def __init__(self, doc_id=None, future_doc_id=None, **kwargs):
        self._doc_id = doc_id
        self._future_doc_id = future_doc_id
        self._lock = defer.DeferredLock()
        super(SoledadDocumentWrapper, self).__init__(**kwargs)

    @property
    def doc_id(self):
        return self._doc_id

    @property
    def future_doc_id(self):
        return self._future_doc_id

    def set_future_doc_id(self, doc_id):
        self._future_doc_id = doc_id

    @defer.inlineCallbacks
    def create(self, store, is_copy=False):
        """
        Create the documents for this wrapper.
        Since this method will not check for duplication, the
        responsibility of avoiding duplicates is left to the caller.

        You might be interested in using `get_or_create` classmethod
        instead (that's the preferred way of creating documents from
        the wrapper object).

        :return: a deferred that will fire when the underlying
                 Soledad document has been created.
        :rtype: Deferred
        """
        assert self.doc_id is None, "This document already has a doc_id!"

        try:
            if self.future_doc_id is None:
                newdoc = yield store.create_doc(
                    self.serialize())
            else:
                newdoc = yield store.create_doc(
                    self.serialize(), doc_id=self.future_doc_id)
            self._doc_id = newdoc.doc_id
            self.set_future_doc_id(None)
        except l2db.errors.RevisionConflict:
            if is_copy:
                # In the case of some copies (for instance, from one folder to
                # another and back to the original folder), the document that
                # we want to insert already exists. In this  case, putting it
                # and overwriting the document with that doc_id is the right
                # thing to do.
                self._doc_id = self.future_doc_id
                self._future_doc_id = None
                yield self.update(store)
            else:
                self.log.warn(
                    'Revision conflict, ignoring: %s' % self.future_doc_id)
        except Exception as exc:
            self.log.warn('Error while creating %s: %r' % (
                self.future_doc_id, exc))

        defer.returnValue(self)

    def update(self, store):
        """
        Update the documents for this wrapper.

        :return: a deferred that will fire when the underlying
                 Soledad document has been updated.
        :rtype: Deferred
        """
        # the deferred lock guards against revision conflicts
        return self._lock.run(self._update, store)

    def _update(self, store):
        assert self._doc_id is not None, "Need to create doc before updating"

        def log_error(failure, doc_id):
            self.log.warn('Error while updating %s' % doc_id)

        def update_and_put_doc(doc):
            doc.content.update(self.serialize())
            d = store.put_doc(doc)
            d.addErrback(log_error, doc.doc_id)
            return d

        d = store.get_doc(self._doc_id)
        d.addCallback(update_and_put_doc)
        return d

    def delete(self, store):
        """
        Delete the documents for this wrapper.

        :return: a deferred that will fire when the underlying
                 Soledad document has been deleted.
        :rtype: Deferred
        """
        # the deferred lock guards against conflicts while updating
        return self._lock.run(self._delete, store)

    def _delete(self, store):
        leap_assert(self._doc_id is not None,
                    "Need to create doc before deleting")
        # XXX might want to flag this DocumentWrapper to avoid
        # updating it by mistake. This could go in models.DocumentWrapper

        def delete_doc(doc):
            return store.delete_doc(doc)

        d = store.get_doc(self._doc_id)
        d.addCallback(delete_doc)
        return d

    @classmethod
    def get_or_create(cls, store, index, value):
        """
        Get a unique DocumentWrapper by index, or create a new one if the
        matching query does not exist.

        :param index: the primary index for the model.
        :type index: str
        :param value: the value to query the primary index.
        :type value: str

        :return: a deferred that will be fired with the SoledadDocumentWrapper
                 matching the index query, either existing or just created.
        :rtype: Deferred
        """
        return cls._get_klass_lock().run(
            cls._get_or_create, store, index, value)

    @classmethod
    def _get_or_create(cls, store, index, value):
        # TODO shorten this method.
        assert store is not None
        assert index is not None
        assert value is not None

        def get_main_index():
            try:
                return cls.model.__meta__.index
            except AttributeError:
                raise RuntimeError("The model is badly defined")

        # TODO separate into another method?
        def try_to_get_doc_from_index(indexes):
            values = []
            idx_def = dict(indexes)[index]
            if len(idx_def) == 1:
                values = [value]
            else:
                main_index = get_main_index()
                fields = cls.model.serialize()
                for field in idx_def:
                    if field == main_index:
                        values.append(value)
                    else:
                        values.append(fields[field])
            d = store.get_from_index(index, *values)
            return d

        def get_first_doc_if_any(docs):
            if not docs:
                return None
            if len(docs) > 1:
                raise DuplicatedDocumentError
            return docs[0]

        def wrap_existing_or_create_new(doc):
            if doc:
                return cls(doc_id=doc.doc_id, **doc.content)
            else:
                return create_and_wrap_new_doc()

        def create_and_wrap_new_doc():
            # XXX use closure to store indexes instead of
            # querying for them again.
            d = store.list_indexes()
            d.addCallback(get_wrapper_instance_from_index)
            d.addCallback(return_wrapper_when_created)
            return d

        def get_wrapper_instance_from_index(indexes):
            init_values = {}
            idx_def = dict(indexes)[index]
            if len(idx_def) == 1:
                init_value = {idx_def[0]: value}
                return cls(**init_value)
            main_index = get_main_index()
            fields = cls.model.serialize()
            for field in idx_def:
                if field == main_index:
                    init_values[field] = value
                else:
                    init_values[field] = fields[field]
            return cls(**init_values)

        def return_wrapper_when_created(wrapper):
            d = wrapper.create(store)
            d.addCallback(lambda doc: wrapper)
            return d

        d = store.list_indexes()
        d.addCallback(try_to_get_doc_from_index)
        d.addCallback(get_first_doc_if_any)
        d.addCallback(wrap_existing_or_create_new)
        return d

    @classmethod
    def get_all(cls, store):
        """
        Get a collection of wrappers around all the documents belonging
        to this kind.

        For this to work, the model.__meta__ needs to include a tuple with
        the index to be used for listing purposes, and which is the field to be
        used to query the index.

        Note that this method only supports indexes of a single field at the
        moment. It also might be too expensive to return all the documents
        matching the query, so handle with care.

        class __meta__(object):
            index = "name"
            list_index = ("by-type", "type_")

        :return: a deferred that will be fired with an iterable containing
                 as many SoledadDocumentWrapper are matching the index defined
                 in the model as the `list_index`.
        :rtype: Deferred
        """
        # TODO LIST (get_all)
        # [ ] extend support to indexes with n-ples
        # [ ] benchmark the cost of querying and returning indexes in a big
        #     database. This might badly need pagination before being put to
        #     serious use.
        return cls._get_klass_lock().run(cls._get_all, store)

    @classmethod
    def _get_all(cls, store):
        try:
            list_index, list_attr = cls.model.__meta__.list_index
        except AttributeError:
            raise RuntimeError("The model is badly defined: no list_index")
        try:
            index_value = getattr(cls.model, list_attr)
        except AttributeError:
            raise RuntimeError("The model is badly defined: "
                               "no attribute matching list_index")

        def wrap_docs(docs):
            return (cls(doc_id=doc.doc_id, **doc.content) for doc in docs)

        d = store.get_from_index(list_index, index_value)
        d.addCallback(wrap_docs)
        return d

    def __repr__(self):
        try:
            idx = getattr(self, self.model.__meta__.index)
        except AttributeError:
            idx = ""
        return "<%s: %s (%s)>" % (self.__class__.__name__,
                                  idx, self._doc_id)


#
# Message documents
#

class FlagsDocWrapper(SoledadDocumentWrapper):

    class model(models.SerializableModel):
        type_ = "flags"
        chash = ""

        mbox_uuid = ""
        seen = False
        deleted = False
        recent = False
        flags = []
        tags = []
        size = 0
        multi = False

        class __meta__(object):
            index = "mbox"

    def set_mbox_uuid(self, mbox_uuid):
        # XXX raise error if already created, should use copy instead
        mbox_uuid = mbox_uuid.replace('-', '_')
        new_id = constants.FDOCID.format(mbox_uuid=mbox_uuid, chash=self.chash)
        self._future_doc_id = new_id
        self.mbox_uuid = mbox_uuid

    def get_flags(self):
        """
        Get the flags for this message (as a tuple of strings, not unicode).
        """
        return map(str, self.flags)


class HeaderDocWrapper(SoledadDocumentWrapper):

    class model(models.SerializableModel):
        type_ = "head"
        chash = ""

        date = ""
        subject = ""
        headers = {}
        part_map = {}
        body = ""  # link to phash of body
        msgid = ""
        multi = False

        class __meta__(object):
            index = "chash"


class ContentDocWrapper(SoledadDocumentWrapper):

    class model(models.SerializableModel):
        type_ = "cnt"
        phash = ""

        ctype = ""  # XXX index by ctype too?
        lkf = []  # XXX not implemented yet!
        raw = ""

        content_disposition = ""
        content_transfer_encoding = ""
        content_type = ""
        charset = ""

        class __meta__(object):
            index = "phash"


class MetaMsgDocWrapper(SoledadDocumentWrapper):

    class model(models.SerializableModel):
        type_ = "meta"
        fdoc = ""
        hdoc = ""
        cdocs = []

    def set_mbox_uuid(self, mbox_uuid):
        # XXX raise error if already created, should use copy instead
        mbox_uuid = mbox_uuid.replace('-', '_')
        chash = re.findall(constants.FDOCID_CHASH_RE, self.fdoc)[0]
        new_id = constants.METAMSGID.format(mbox_uuid=mbox_uuid, chash=chash)
        new_fdoc_id = constants.FDOCID.format(mbox_uuid=mbox_uuid, chash=chash)
        self._future_doc_id = new_id
        self.fdoc = new_fdoc_id


class MessageWrapper(object):

    # This could benefit of a DeferredLock to create/update all the
    # documents at the same time maybe, and defend against concurrent updates?

    implements(IMessageWrapper)
    log = Logger()

    def __init__(self, mdoc, fdoc, hdoc, cdocs=None, is_copy=False):
        """
        Need at least a metamsg-document, a flag-document and a header-document
        to instantiate a MessageWrapper. Content-documents can be retrieved
        lazily.

        cdocs, if any, should be a dictionary in which the keys are ascending
        integers, beginning at one, and the values are dictionaries with the
        content of the content-docs.

        is_copy, if set to True, will only attempt to create mdoc and fdoc
        (because hdoc and cdocs are supposed to exist already)
        """
        self._is_copy = is_copy

        def get_doc_wrapper(doc, cls):
            if isinstance(doc, SoledadDocument):
                doc_id = doc.doc_id
                doc = doc.content
            else:
                doc_id = None
            if not doc:
                doc = {}
            return cls(doc_id=doc_id, **doc)

        self.mdoc = get_doc_wrapper(mdoc, MetaMsgDocWrapper)

        self.fdoc = get_doc_wrapper(fdoc, FlagsDocWrapper)
        self.fdoc.set_future_doc_id(self.mdoc.fdoc)

        self.hdoc = get_doc_wrapper(hdoc, HeaderDocWrapper)
        self.hdoc.set_future_doc_id(self.mdoc.hdoc)

        if cdocs is None:
            cdocs = {}
        cdocs_keys = cdocs.keys()
        assert sorted(cdocs_keys) == range(1, len(cdocs_keys) + 1)
        self.cdocs = dict([
            (key, get_doc_wrapper(doc, ContentDocWrapper))
            for (key, doc) in cdocs.items()])
        for doc_id, cdoc in zip(self.mdoc.cdocs, self.cdocs.values()):
            if cdoc.raw == "":
                self.log.warn('Empty raw field in cdoc %s' % doc_id)
            cdoc.set_future_doc_id(doc_id)

    @defer.inlineCallbacks
    def create(self, store):
        """
        Create all the parts for this message in the store.

        :param store: an instance of Soledad

        :return: a deferred whose callback will be called when all the
                 part documents have been written.
        :rtype: defer.Deferred
        """
        assert self.cdocs, "Need cdocs to create the MessageWrapper docs"
        assert self.mdoc.doc_id is None, "Cannot create: mdoc has a doc_id"
        assert self.fdoc.doc_id is None, "Cannot create: fdoc has a doc_id"

        copy = self._is_copy

        mdoc = yield self.mdoc.create(store, is_copy=copy)
        assert mdoc
        self.mdoc = mdoc
        fdoc = yield self.fdoc.create(store, is_copy=copy)
        self.fdoc = fdoc
        if not copy:
            if self.hdoc.doc_id is None:
                hdoc = yield self.hdoc.create(store)
                self.hdoc = hdoc
            for cdoc in self.cdocs.values():
                if cdoc.doc_id is not None:
                    # we could be just linking to an existing
                    # content-doc.
                    continue
                yield cdoc.create(store)
        defer.returnValue(self)

    def update(self, store):
        """
        Update the only mutable parts, which are within the flags document.
        """
        return self.fdoc.update(store)

    def delete(self, store):
        # TODO
        # Eventually this would have to do the duplicate search or send for the
        # garbage collector. At least mdoc and t the mdoc and fdoc can be
        # unlinked.
        d = []
        if self.mdoc.doc_id:
            d.append(self.mdoc.delete(store))
        d.append(self.fdoc.delete(store))
        return defer.gatherResults(d)

    def copy(self, store, new_mbox_uuid):
        """
        Return a copy of this MessageWrapper in a new mailbox.

        :param store: an instance of Soledad, or anything that behaves alike.
        :param new_mbox_uuid: the uuid of the mailbox where we are copying this
               message to.
        :type new_mbox_uuid: str
        :rtype: MessageWrapper
        """
        new_mdoc = self.mdoc.serialize()
        new_fdoc = self.fdoc.serialize()

        # the future doc_ids is properly set because we modified
        # the pointers in mdoc, which has precedence.
        new_wrapper = MessageWrapper(new_mdoc, new_fdoc, None, None,
                                     is_copy=True)
        new_wrapper.hdoc = self.hdoc
        new_wrapper.cdocs = self.cdocs
        new_wrapper.set_mbox_uuid(new_mbox_uuid)

        # XXX could flag so that it only creates mdoc/fdoc...

        d = new_wrapper.create(store)
        d.addCallback(lambda result: new_wrapper)
        return d

    def set_mbox_uuid(self, mbox_uuid):
        """
        Set the mailbox for this wrapper.
        This method should only be used before the Documents for the
        MessageWrapper have been created, will raise otherwise.
        """
        mbox_uuid = mbox_uuid.replace('-', '_')
        self.mdoc.set_mbox_uuid(mbox_uuid)
        self.fdoc.set_mbox_uuid(mbox_uuid)

    def set_flags(self, flags):
        # TODO serialize the get + update
        if flags is None:
            flags = tuple()
        leap_assert_type(flags, tuple)
        self.fdoc.flags = list(flags)
        self.fdoc.deleted = "\\Deleted" in flags
        self.fdoc.seen = "\\Seen" in flags
        self.fdoc.recent = "\\Recent" in flags

    def set_tags(self, tags):
        # TODO serialize the get + update
        if tags is None:
            tags = tuple()
        leap_assert_type(tags, tuple)
        self.fdoc.tags = list(tags)

    def set_date(self, date):
        # XXX assert valid date format
        self.hdoc.date = date

    def get_subpart_dict(self, index):
        """
        :param index: the part to lookup, 1-indexed
        :type index: int
        :rtype: dict
        """
        return self.hdoc.part_map[str(index)]

    def get_subpart_indexes(self):
        return self.hdoc.part_map.keys()

    def get_body(self, store):
        """
        :rtype: deferred
        """
        body_phash = self.hdoc.body
        if body_phash:
            d = store.get_doc('C-' + body_phash)
            d.addCallback(lambda doc: ContentDocWrapper(**doc.content))
            return d
        elif self.cdocs:
            return self.cdocs[1]
        else:
            return ''

#
# Mailboxes
#


class MailboxWrapper(SoledadDocumentWrapper):

    class model(models.SerializableModel):
        type_ = "mbox"
        mbox = INBOX_NAME
        uuid = None
        flags = []
        recent = []
        created = 1
        closed = False
        subscribed = False

        class __meta__(object):
            index = "mbox"
            list_index = (indexes.TYPE_IDX, 'type_')


#
# Soledad Adaptor
#

class SoledadIndexMixin(object):
    """
    This will need a class attribute `indexes`, that is a dictionary containing
    the index definitions for the underlying l2db store underlying soledad.

    It needs to be in the following format:
    {'index-name': ['field1', 'field2']}

    You can also add a class attribute `wait_for_indexes` to any class
    inheriting from this Mixin, that should be a list of strings representing
    the methods that need to wait until the indexes have been initialized
    before being able to work properly.
    """
    # TODO move this mixin to soledad itself
    # so that each application can pass a set of indexes for their data model.

    # TODO could have a wrapper class for indexes, supporting introspection
    # and __getattr__

    # TODO make this an interface?

    indexes = {}
    wait_for_indexes = []
    store_ready = False

    def initialize_store(self, store):
        """
        Initialize the indexes in the database.

        :param store: store
        :returns: a Deferred that will fire when the store is correctly
                  initialized.
        :rtype: deferred
        """
        # TODO I think we *should* get another deferredLock in here, but
        # global to the soledad namespace, to protect from several points
        # initializing soledad indexes at the same time.
        self._wait_for_indexes()

        d = self._init_indexes(store)
        d.addCallback(self._restore_waiting_methods)
        return d

    def _init_indexes(self, store):
        """
        Initialize the database indexes.
        """
        leap_assert(store, "Cannot init indexes with null soledad")
        leap_assert_type(self.indexes, dict)

        def _create_index(name, expression):
            return store.create_index(name, *expression)

        def init_idexes(indexes):
            deferreds = []
            db_indexes = dict(indexes)
            # Loop through the indexes we expect to find.
            for name, expression in self.indexes.items():
                if name not in db_indexes:
                    # The index does not yet exist.
                    d = _create_index(name, expression)
                    deferreds.append(d)
                elif expression != db_indexes[name]:
                    # The index exists but the definition is not what expected,
                    # so we delete it and add the proper index expression.
                    d = store.delete_index(name)
                    d.addCallback(
                        lambda _: _create_index(name, *expression))
                    deferreds.append(d)
            return defer.gatherResults(deferreds, consumeErrors=True)

        def store_ready(whatever):
            self.store_ready = True
            return whatever

        self.deferred_indexes = store.list_indexes()
        self.deferred_indexes.addCallback(init_idexes)
        self.deferred_indexes.addCallback(store_ready)
        return self.deferred_indexes

    def _wait_for_indexes(self):
        """
        Make the marked methods to wait for the indexes to be ready.
        Heavily based on
        http://blogs.fluidinfo.com/terry/2009/05/11/a-mixin-class-allowing-python-__init__-methods-to-work-with-twisted-deferreds/

        :param methods: methods that need to wait for the indexes to be ready
        :type methods: tuple(str)
        """
        leap_assert_type(self.wait_for_indexes, list)
        methods = self.wait_for_indexes

        self.waiting = []
        self.stored = {}

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

    def _restore_waiting_methods(self, _):
        for method in self.stored:
            setattr(self, method, self.stored[method])
        for d in self.waiting:
            d.callback(None)


class SoledadMailAdaptor(SoledadIndexMixin):

    implements(IMailAdaptor)
    store = None

    indexes = indexes.MAIL_INDEXES
    wait_for_indexes = ['get_or_create_mbox', 'update_mbox', 'get_all_mboxes']

    mboxwrapper_klass = MailboxWrapper
    atomic = defer.DeferredLock()

    log = Logger()

    def __init__(self):
        SoledadIndexMixin.__init__(self)

    # Message handling

    def get_msg_from_string(self, MessageClass, raw_msg):
        """
        Get an instance of a MessageClass initialized with a MessageWrapper
        that contains all the parts obtained from parsing the raw string for
        the message.

        :param MessageClass: any Message class that can be initialized passing
                             an instance of an IMessageWrapper implementor.
        :type MessageClass: type
        :param raw_msg: a string containing the raw email message.
        :type raw_msg: str
        :rtype: MessageClass instance.
        """
        assert(MessageClass is not None)
        mdoc, fdoc, hdoc, cdocs = _split_into_parts(raw_msg)
        return self.get_msg_from_docs(
            MessageClass, mdoc, fdoc, hdoc, cdocs)

    def get_msg_from_docs(self, MessageClass, mdoc, fdoc, hdoc, cdocs=None,
                          uid=None):
        """
        Get an instance of a MessageClass initialized with a MessageWrapper
        that contains the passed part documents.

        This is not the recommended way of obtaining a message, unless you know
        how to take care of ensuring the internal consistency between the part
        documents, or unless you are glueing together the part documents that
        have been previously generated by `get_msg_from_string`.

        :param MessageClass: any Message class that can be initialized passing
                             an instance of an IMessageWrapper implementor.
        :type MessageClass: type
        :param fdoc: a dictionary containing values from which a
                     FlagsDocWrapper can be initialized
        :type fdoc: dict
        :param hdoc: a dictionary containing values from which a
                     HeaderDocWrapper can be initialized
        :type hdoc: dict
        :param cdocs: None, or a dictionary mapping integers (1-indexed) to
                      dicts from where a ContentDocWrapper can be initialized.
        :type cdocs: dict, or None

        :rtype: MessageClass instance.
        """
        assert(MessageClass is not None)
        return MessageClass(MessageWrapper(mdoc, fdoc, hdoc, cdocs), uid=uid)

    def get_msg_from_mdoc_id(self, MessageClass, store, mdoc_id,
                             uid=None, get_cdocs=False):

        def wrap_meta_doc(doc):
            cls = MetaMsgDocWrapper
            return cls(doc_id=doc.doc_id, **doc.content)

        def get_part_docs_from_mdoc_wrapper(wrapper):
            d_docs = []
            d_docs.append(store.get_doc(wrapper.fdoc))
            d_docs.append(store.get_doc(wrapper.hdoc))
            for cdoc in wrapper.cdocs:
                d_docs.append(store.get_doc(cdoc))

            def add_mdoc(doc_list):
                return [wrapper.serialize()] + doc_list

            d = defer.gatherResults(d_docs)
            d.addCallback(add_mdoc)
            return d

        def get_parts_doc_from_mdoc_id():
            mbox = re.findall(constants.METAMSGID_MBOX_RE, mdoc_id)[0]
            chash = re.findall(constants.METAMSGID_CHASH_RE, mdoc_id)[0]

            def _get_fdoc_id_from_mdoc_id():
                return constants.FDOCID.format(mbox_uuid=mbox, chash=chash)

            def _get_hdoc_id_from_mdoc_id():
                return constants.HDOCID.format(mbox_uuid=mbox, chash=chash)

            d_docs = []
            fdoc_id = _get_fdoc_id_from_mdoc_id()
            hdoc_id = _get_hdoc_id_from_mdoc_id()

            d_docs.append(store.get_doc(mdoc_id))
            d_docs.append(store.get_doc(fdoc_id))
            d_docs.append(store.get_doc(hdoc_id))

            d = defer.gatherResults(d_docs)
            return d

        def _err_log_failure_part_docs(failure):
            # See https://leap.se/code/issues/7495.
            # This avoids blocks, but the real cause still needs to be
            # isolated (0.9.0rc3) -- kali
            self.log.debug("BUG ------------------------------------------")
            self.log.debug(
                "BUG: Error while retrieving part docs for mdoc id %s" %
                mdoc_id)
            self.log.debug("BUG (please report above info) ---------------")
            return []

        def _err_log_cannot_find_msg(failure):
            self.log.error('BUG: Error while getting msg (uid=%s)' % uid)
            return None

        if get_cdocs:
            d = store.get_doc(mdoc_id)
            d.addCallback(wrap_meta_doc)
            d.addCallback(get_part_docs_from_mdoc_wrapper)
            d.addErrback(_err_log_failure_part_docs)

        else:
            d = get_parts_doc_from_mdoc_id()

        d.addCallback(self._get_msg_from_variable_doc_list,
                      msg_class=MessageClass, uid=uid)
        d.addErrback(_err_log_cannot_find_msg)
        return d

    def _get_msg_from_variable_doc_list(self, doc_list, msg_class, uid=None):
        if len(doc_list) == 3:
            mdoc, fdoc, hdoc = doc_list
            cdocs = None
        elif len(doc_list) > 3:
            # XXX is this case used?
            mdoc, fdoc, hdoc = doc_list[:3]
            cdocs = dict(enumerate(doc_list[3:], 1))
        return self.get_msg_from_docs(
            msg_class, mdoc, fdoc, hdoc, cdocs, uid=uid)

    def get_flags_from_mdoc_id(self, store, mdoc_id):
        """
        # XXX stuff here...
        """
        mbox = re.findall(constants.METAMSGID_MBOX_RE, mdoc_id)[0]
        chash = re.findall(constants.METAMSGID_CHASH_RE, mdoc_id)[0]

        def _get_fdoc_id_from_mdoc_id():
            return constants.FDOCID.format(mbox_uuid=mbox, chash=chash)

        fdoc_id = _get_fdoc_id_from_mdoc_id()

        def wrap_fdoc(doc):
            if not doc:
                return
            cls = FlagsDocWrapper
            return cls(doc_id=doc.doc_id, **doc.content)

        def get_flags(fdoc_wrapper):
            if not fdoc_wrapper:
                return []
            return fdoc_wrapper.get_flags()

        d = store.get_doc(fdoc_id)
        d.addCallback(wrap_fdoc)
        d.addCallback(get_flags)
        return d

    def create_msg(self, store, msg):
        """
        :param store: an instance of soledad, or anything that behaves alike
        :param msg: a Message object.

        :return: a Deferred that is fired when all the underlying documents
                 have been created.
        :rtype: defer.Deferred
        """
        wrapper = msg.get_wrapper()
        return wrapper.create(store)

    def update_msg(self, store, msg):
        """
        :param msg: a Message object.
        :param store: an instance of soledad, or anything that behaves alike
        :return: a Deferred that is fired when all the underlying documents
                 have been updated (actually, it's only the fdoc that's allowed
                 to update).
        :rtype: defer.Deferred
        """
        wrapper = msg.get_wrapper()
        return wrapper.update(store)

    # batch deletion

    def del_all_flagged_messages(self, store, mbox_uuid):
        """
        Delete all messages flagged as deleted.
        """

        def delete_fdoc_and_mdoc_flagged(fdocs):
            # low level here, not using the wrappers...
            # get meta doc ids from the flag doc ids
            fdoc_ids = [doc.doc_id for doc in fdocs]
            mdoc_ids = map(lambda s: "M" + s[1:], fdoc_ids)

            def delete_all_docs(mdocs, fdocs):
                mdocs = list(mdocs)
                doc_ids = [m.doc_id for m in mdocs]
                _d = []
                docs = mdocs + fdocs
                for doc in docs:
                    _d.append(store.delete_doc(doc))
                d = defer.gatherResults(_d)
                # return the mdocs ids only
                d.addCallback(lambda _: doc_ids)
                return d

            d = store.get_docs(mdoc_ids)
            d.addCallback(delete_all_docs, fdocs)
            return d

        type_ = FlagsDocWrapper.model.type_
        uuid = mbox_uuid.replace('-', '_')
        deleted_index = indexes.TYPE_MBOX_DEL_IDX

        d = store.get_from_index(deleted_index, type_, uuid, "1")
        d.addCallback(delete_fdoc_and_mdoc_flagged)
        return d

    # count messages

    def get_count_unseen(self, store, mbox_uuid):
        """
        Get the number of unseen messages for a given mailbox.

        :param store: instance of Soledad.
        :param mbox_uuid: the uuid for this mailbox.
        :rtype: int
        """
        type_ = FlagsDocWrapper.model.type_
        uuid = mbox_uuid.replace('-', '_')

        unseen_index = indexes.TYPE_MBOX_SEEN_IDX

        d = store.get_count_from_index(unseen_index, type_, uuid, "0")
        d.addErrback(lambda f: self.log.error('Error on count_unseen'))
        return d

    def get_count_recent(self, store, mbox_uuid):
        """
        Get the number of recent messages for a given mailbox.

        :param store: instance of Soledad.
        :param mbox_uuid: the uuid for this mailbox.
        :rtype: int
        """
        type_ = FlagsDocWrapper.model.type_
        uuid = mbox_uuid.replace('-', '_')

        recent_index = indexes.TYPE_MBOX_RECENT_IDX

        d = store.get_count_from_index(recent_index, type_, uuid, "1")
        d.addErrback(lambda f: self.log.error('Error on count_recent'))
        return d

    # search api

    def get_mdoc_id_from_msgid(self, store, mbox_uuid, msgid):
        """
        Get the UID for a message with the passed msgid (the one in the headers
        msg-id).
        This is used by the MUA to retrieve the recently saved draft.
        """
        type_ = HeaderDocWrapper.model.type_
        uuid = mbox_uuid.replace('-', '_')

        msgid_index = indexes.TYPE_MSGID_IDX

        def get_mdoc_id(hdoc):
            if not hdoc:
                self.log.warn("Could not find a HDOC with MSGID %s" % msgid)
                return None
            hdoc = hdoc[0]
            mdoc_id = hdoc.doc_id.replace("H-", "M-%s-" % uuid)
            return mdoc_id

        d = store.get_from_index(msgid_index, type_, msgid)
        d.addCallback(get_mdoc_id)
        return d

    # Mailbox handling

    def get_or_create_mbox(self, store, name):
        """
        Get the mailbox with the given name, or create one if it does not
        exist.

        :param store: instance of Soledad
        :param name: the name of the mailbox
        :type name: str
        """
        index = indexes.TYPE_MBOX_IDX
        mbox = normalize_mailbox(name)
        return MailboxWrapper.get_or_create(store, index, mbox)

    def update_mbox(self, store, mbox_wrapper):
        """
        Update the documents for a given mailbox.
        :param mbox_wrapper: MailboxWrapper instance
        :type mbox_wrapper: MailboxWrapper
        :return: a Deferred that will be fired when the mailbox documents
                 have been updated.
        :rtype: defer.Deferred
        """
        leap_assert_type(mbox_wrapper, SoledadDocumentWrapper)
        return mbox_wrapper.update(store)

    def delete_mbox(self, store, mbox_wrapper):
        leap_assert_type(mbox_wrapper, SoledadDocumentWrapper)
        return mbox_wrapper.delete(store)

    def get_all_mboxes(self, store):
        """
        Retrieve a list with wrappers for all the mailboxes.

        :return: a deferred that will be fired with a list of all the
                 MailboxWrappers found.
        :rtype: defer.Deferred
        """
        return MailboxWrapper.get_all(store)


def _split_into_parts(raw):
    # TODO signal that we can delete the original message!-----
    # when all the processing is done.
    # TODO add the linked-from info !
    # TODO add reference to the original message?
    # TODO populate Default FLAGS/TAGS (unseen?)
    # TODO seed propely the content_docs with defaults??

    msg, chash, multi = _parse_msg(raw)
    size = len(msg.as_string())

    parts_map = walk.get_tree(msg)
    cdocs_list = list(walk.get_raw_docs(msg))
    cdocs_phashes = [c['phash'] for c in cdocs_list]
    body_phash = walk.get_body_phash(msg)

    mdoc = _build_meta_doc(chash, cdocs_phashes)
    fdoc = _build_flags_doc(chash, size, multi)
    hdoc = _build_headers_doc(msg, chash, body_phash, parts_map)

    # The MessageWrapper expects a dict, one-indexed
    cdocs = dict(enumerate(cdocs_list, 1))

    return mdoc, fdoc, hdoc, cdocs


def _parse_msg(raw):
    msg = message_from_string(raw)
    chash = walk.get_hash(raw)
    multi = msg.is_multipart()
    return msg, chash, multi


def _build_meta_doc(chash, cdocs_phashes):
    _mdoc = MetaMsgDocWrapper()
    # FIXME passing the inbox name because we don't have the uuid at this
    # point.

    _mdoc.fdoc = constants.FDOCID.format(mbox_uuid=INBOX_NAME, chash=chash)
    _mdoc.hdoc = constants.HDOCID.format(chash=chash)
    _mdoc.cdocs = [constants.CDOCID.format(phash=p) for p in cdocs_phashes]

    return _mdoc.serialize()


def _build_flags_doc(chash, size, multi):
    _fdoc = FlagsDocWrapper(chash=chash, size=size, multi=multi)
    return _fdoc.serialize()


def _build_headers_doc(msg, chash, body_phash, parts_map):
    """
    Assemble a headers document from the original parsed message, the
    content-hash, and the parts map.

    It takes into account possibly repeated headers.
    """
    headers = defaultdict(list)
    for k, v in msg.items():
        headers[k].append(v)
    # "fix" for repeated headers (as in "Received:"
    for k, v in headers.items():
        newline = "\n%s: " % (k.lower(),)
        headers[k] = newline.join(v)

    lower_headers = lowerdict(dict(headers))
    msgid = first(_MSGID_RE.findall(
        lower_headers.get('message-id', '')))

    _hdoc = HeaderDocWrapper(
        chash=chash, headers=headers, body=body_phash,
        msgid=msgid)

    def copy_attr(headers, key, doc):
        if key in headers:
            setattr(doc, key, headers[key])

    copy_attr(lower_headers, "subject", _hdoc)
    copy_attr(lower_headers, "date", _hdoc)

    hdoc = _hdoc.serialize()
    # add some of the attr from the parts map to header doc
    for key in parts_map:
        if key in ('body', 'multi', 'part_map'):
            hdoc[key] = parts_map[key]
    return stringify_parts_map(hdoc)
