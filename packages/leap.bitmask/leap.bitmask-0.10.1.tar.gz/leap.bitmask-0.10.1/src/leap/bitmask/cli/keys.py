# -*- coding: utf-8 -*-
# keys
# Copyright (C) 2016 LEAP
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
Bitmask Command Line interface: keys
"""
import argparse
import sys

from colorama import Fore

from leap.bitmask.cli import command

try:
    from leap.bitmask.keymanager.validation import ValidationLevels
    HAS_KM = True
except ImportError:
    HAS_KM = False


class Keys(command.Command):
    service = 'keys'
    usage = '''{name} keys <subcommand>

Bitmask Keymanager management service

SUBCOMMANDS:

   list       List all known keys
   export     Export a given key
   insert     Insert a key to the key storage
   delete     Delete a key from the key storage
'''.format(name=command.appname)

    def list(self, raw_args):
        parser = argparse.ArgumentParser(
            description='Bitmask list keys',
            prog='%s %s %s' % tuple(sys.argv[:3]))
        parser.add_argument('-u', '--userid', default='',
                            help='Select the userid of the keyring')
        parser.add_argument('--private', action='store_true',
                            help='Use private keys (by default uses public)')
        subargs = parser.parse_args(raw_args)

        userid = subargs.userid
        if not userid:
            userid = self.cfg.get('bonafide', 'active', default='')

        self.data += ['list', userid]
        if subargs.private:
            self.data += ['private']
        else:
            self.data += ['public']

        return self._send(self._print_key_list)

    def export(self, raw_args):
        parser = argparse.ArgumentParser(
            description='Bitmask export key',
            prog='%s %s %s' % tuple(sys.argv[:3]))
        parser.add_argument('-u', '--userid', default='',
                            help='Select the userid of the keyring')
        parser.add_argument('--private', action='store_true',
                            help='Use private keys (by default uses public)')
        parser.add_argument('--fetch', action='store_true',
                            help='Try to fetch remotely the key if it is not '
                            'in the local storage')
        parser.add_argument('address', nargs=1,
                            help='email address of the key')
        subargs = parser.parse_args(raw_args)

        userid = subargs.userid
        if not userid:
            userid = self.cfg.get('bonafide', 'active', default='')
        self.data += ['export', userid, subargs.address[0]]

        if subargs.private and subargs.fetch:
            print('Cannot fetch private keys')
            return
        if subargs.private:
            self.data += ['private']
        if subargs.fetch:
            self.data += ['fetch']

        return self._send(self._print_key)

    def insert(self, raw_args):
        parser = argparse.ArgumentParser(
            description='Bitmask import key',
            prog='%s %s %s' % tuple(sys.argv[:3]))
        parser.add_argument('-u', '--userid', default='',
                            help='Select the userid of the keyring')
        parser.add_argument('--validation', choices=list(ValidationLevels),
                            default='Fingerprint',
                            help='Validation level for the key')
        parser.add_argument('file', nargs=1,
                            help='file where the key is stored')
        parser.add_argument('address', nargs=1,
                            help='email address of the key')
        subargs = parser.parse_args(raw_args)

        userid = subargs.userid
        if not userid:
            userid = self.cfg.get('bonafide', 'active')

        with open(subargs.file[0], 'r') as keyfile:
            rawkey = keyfile.read()
        self.data += ['insert', userid, subargs.address[0],
                      subargs.validation, rawkey]

        return self._send(self._print_key)

    def delete(self, raw_args):
        parser = argparse.ArgumentParser(
            description='Bitmask delete key',
            prog='%s %s %s' % tuple(sys.argv[:3]))
        parser.add_argument('-u', '--userid', default='',
                            help='Select the userid of the keyring')
        parser.add_argument('--private', action='store_true',
                            help='Use private keys (by default uses public)')
        parser.add_argument('address', nargs=1,
                            help='email address of the key')
        subargs = parser.parse_args(raw_args)

        userid = subargs.userid
        if not userid:
            userid = self.cfg.get('bonafide', 'active')

        self.data += ['delete', userid, subargs.address[0]]
        if subargs.private:
            self.data += ['private']
        else:
            self.data += ['public']
        return self._send()

    def _print_key_list(self, keys):
        for key in keys:
            print(Fore.GREEN +
                  key["fingerprint"] + " " + key['address'] +
                  Fore.RESET)

    def _print_key(self, key):
        print(Fore.GREEN)
        print("Uids:       " + ', '.join(key['uids']))
        print("Fingerprint:" + key['fingerprint'])
        print("Length:     " + str(key['length']))
        print("Expiration: " + key['expiry_date'])
        print("Validation: " + key['validation'])
        print("Used:       " + "sig:" +
              str(key['sign_used']) + ", encr:" +
              str(key['encr_used']))
        print("Refreshed:   " + key['refreshed_at'])
        print(Fore.RESET)
        print("")
        print(key['key_data'])
