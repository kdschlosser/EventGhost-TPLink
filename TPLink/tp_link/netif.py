# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

class Netif(object):

    def __init__(self, device):
        self.device = device

    def _send(self, **kwargs):
        return self.device.query(netif=kwargs)

    def scan(self, refresh=1):
        """
        Scans for access points.

        :param int refresh: Refresh interval in seconds.
        :return: Returns a list of access points.
        :rtype: list
        :raises SmartPlugException: on error
        """
        return self._send(get_scaninfo=dict(refresh=refresh))['ap_list']

    # TODO: map out the key_types
    def connect(self, ssid='', password='', key_type=3):
        """
        Connects to an access point.

        "ap_list": [
                {
                    "key_type": 2,
                    "ssid": "Hufflepup"
                },
                {
                    "key_type": 1,
                    "ssid": "Schlosser"
                },
                {
                    "key_type": 0,
                    "ssid": "xfinitywifi"
                }
            ],
        key_type 0 = None
        key_type 1 = WEP
        key_type 2 = WPA
        key_type 3 = WPA2
        :param str ssid: Access point ssid.
        :param str password: Access point password.
        :param int key_type: Access point encryption type.
        :return: bool
        :rtype: bool
        :raises SmartPlugException: on error
        """
        return self._send(
            set_stainfo=dict(ssid=ssid, password=password, key_type=key_type)
        )
