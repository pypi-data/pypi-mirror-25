# -*- coding: utf-8 -*-
# windows.py
# Copyright (C) 2013-2017 LEAP
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
Windows VPN launcher implementation.
"""

from twisted.logger import Logger

from leap.bitmask.vpn.launcher import VPNLauncher


logger = get_logger()


class WindowsVPNLauncher(VPNLauncher):
    """
    VPN launcher for the Windows platform
    """

    OPENVPN_BIN = 'openvpn_leap.exe'

    # XXX UPDOWN_FILES ... we do not have updown files defined yet!
    # (and maybe we won't)

    @classmethod
    def get_vpn_command(kls, vpnconfig, providerconfig, socket_host,
                        socket_port="9876", openvpn_verb=1):
        """
        Returns the Windows implementation for the vpn launching command.

        Might raise:
            OpenVPNNotFoundException,
            VPNLauncherException.

        :param vpnconfig: vpn configuration object
        :type vpnconfig: VPNConfig
        :param providerconfig: provider specific configuration
        :type providerconfig: ProviderConfig
        :param socket_host: either socket path (unix) or socket IP
        :type socket_host: str
        :param socket_port: either string "unix" if it's a unix socket,
                            or port otherwise
        :type socket_port: str
        :param openvpn_verb: the openvpn verbosity wanted
        :type openvpn_verb: int

        :return: A VPN command ready to be launched.
        :rtype: list
        """
        # TODO add check for this
        # leap_assert(socket_port != "unix",
        #             "We cannot use unix sockets in windows!")

        # we use `super` in order to send the class to use
        command = super(WindowsVPNLauncher, kls).get_vpn_command(
            vpnconfig, providerconfig, socket_host, socket_port, openvpn_verb)

        return command
