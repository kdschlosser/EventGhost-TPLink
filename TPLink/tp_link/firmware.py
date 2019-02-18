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


class Firmware(object):

    def __init__(self, device):
        self.device = device

    @property
    def id(self):
        try:
            return self.device.system.fwId
        except AttributeError:
            return 'N/A'

    @property
    def version(self):
        try:
            return self.device.system.sw_ver
        except AttributeError:
            return 'N/A'

    @property
    def firmware_list(self):
        """
        Get Firmware List from Cloud Server.

        :return: List of firmwares
        :rtype: list
        :raises SmartPlugException: on error
        """
        if self.url:
            return self.device.cloud._send(get_intl_fw_list=None)['fwDlPage']
        return []

    @property
    def url(self):
        return self.device.cloud._send(get_info=None)['fwDlPage']

    @url.setter
    def url(self, url):
        self.device.system.download_firmware = dict(url=url)

    def flash(self):
        self.device.system.flash_firmware = dict()

    @property
    def download_state(self):
        """
        Gets the firmware download state.

        :return: Download state
        :rtype: str
        :raises SmartPlugException: on error
        """
        return self.device.system.download_state

    @property
    def updating(self):
        try:
            return self.device.system.updating
        except AttributeError:
            return 'N/A'
