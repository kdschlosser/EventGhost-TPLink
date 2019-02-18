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


class Cloud(object):
    """
    "cnCloud": {
            "get_info": {
                "username": "",
                "tcspInfo": "",
                "binded": 0,
                "illegalType": -1,
                "tcspStatus": -1,
                "fwDlPage": "",
                "server": "devs.tplinkcloud.com",
                "stopConnect": -1,
                "fwNotifyType": 0,
                "cld_connection": 0,
                "err_code": 0
            }
        },
    """

    def __init__(self, device):
        self.device = device

    @property
    def _info(self):
        return self._send(get_info=None)

    def _send(self, **kwargs):
        return self.device.query(cnCloud=kwargs)

    @property
    def server(self):
        """
        Get Cloud Info.

        :return: Cloud info Server, Username, Connection Status
        :rtype: dict
        :raises SmartPlugException: on error
        """
        return self._info['server']

    @server.setter
    def server(self, server):
        """
        Set cloud server url.

        :param str server: Server url.
        :return: None
        :rtype: None
        :raises SmartPlugException: on error
        """
        self._send(set_server_url=dict(server=server))

    @property
    def is_connected(self):
        return bool(self._info['cld_connection'])

    @property
    def user(self):
        return self._info['username']

    @property
    def is_bound(self):
        return bool(self._info['binded'])

    def bind(self, username, password):
        """
        Register device on cloud server.

        :param str username: Username.
        :param str password: Password.
        :return: None
        :rtype: None
        :raises SmartPlugException: on error
        """
        self._send(bind=dict(username=username, password=password))

    def unbind(self):
        """
        Unregister device from cloud server.

        :return: None
        :rtype: None
        :raises SmartPlugException: on error
        """
        return self._send(unbind=None)
