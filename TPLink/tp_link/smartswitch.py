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

import _LOGGER
from smartdevice import SmartDeviceBase

# model    e-meter
# HS200     False

# HS200_US = {
#     u'sys_info': {
#         u'emeter': {
#             u'err_code': -1,
#             u'err_msg': u'module not support'
#         },
#         u'system': {
#             u'get_sysinfo': {
#                 u'active_mode': u'schedule',
#                 u'alias': u'Outside Garage Light',
#                 u'dev_name': u'Wi-Fi Smart Light Switch',
#                 u'deviceId': u'',
#                 u'err_code': 0,
#                 u'feature': u'TIM',
#                 u'fwId': u'',
#                 u'hwId': u'',
#                 u'hw_ver': u'1.0',
#                 u'icon_hash': u'',
#                 u'latitude': 0,
#                 u'led_off': 0,
#                 u'longitude': 0,
#                 u'mac': u'',
#                 u'mic_type': u'IOT.SMARTPLUGSWITCH',
#                 u'model': u'HS200(US)',
#                 u'oemId': u'',
#                 u'on_time': 0,
#                 u'relay_state': 0,
#                 u'rssi': -55,
#                 u'sw_ver': u'1.1.0 Build 160521 Rel.085826',
#                 u'updating': 0
#             }
#         }
#     }
# }


class SmartSwitch(SmartDeviceBase):
    """Representation of a TP-Link Smart Plug.

    Usage example when used as library:
    p = SmartPlug("192.168.1.105")
    # print the devices alias
    print(p.alias)
    # change state of plug
    p.state = "ON"
    p.state = "OFF"
    # query and print current state of plug
    print(p.state)

    Errors reported by the device are raised as SmartPlugExceptions,
    and should be handled by the user of the library.

    Note:
    The library references the same structure as defined for the D-Link Switch
    """

    SWITCH_STATE_ON = 'ON'
    SWITCH_STATE_OFF = 'OFF'
    SWITCH_STATE_UNKNOWN = 'UNKNOWN'

    LED_STATE_ON = 'ON'
    LED_STATE_OFF = 'OFF'

    @property
    def state(self):
        """
        Retrieve the switch state

        :returns: one of
                  instance.SWITCH_STATE_ON
                  instance.SWITCH_STATE_OFF
                  instance.SWITCH_STATE_UNKNOWN
        :rtype: str
        """
        relay_state = self.system.relay_state

        if relay_state == 0:
            return self.SWITCH_STATE_OFF
        elif relay_state == 1:
            return self.SWITCH_STATE_ON
        else:
            _LOGGER.warning("Unknown state %s returned.", relay_state)
            return self.SWITCH_STATE_UNKNOWN

    @state.setter
    def state(self, flag):
        """
        Set the new switch state

        :param flag: one of
                    instance.SWITCH_STATE_ON
                    instance.SWITCH_STATE_OFF
        :raises ValueError: on invalid state
        :raises SmartPlugException: on error

        """

        flag = str(flag)

        if flag in ('1', self.SWITCH_STATE_ON):
            self.turn_on()
        elif flag in ('0', self.SWITCH_STATE_OFF):
            self.turn_off()
        else:
            raise ValueError("State %s is not valid.", flag)

    @property
    def is_on(self):
        """
        Returns whether device is on.

        :return: True if device is on, False otherwise
        """
        return bool(self.system.relay_state)

    @property
    def is_off(self):
        """
        Returns whether device is off.

        :return: True if device is off, False otherwise.
         :rtype: bool
        """
        return not self.is_on

    def turn_on(self):
        """
        Turn the switch on.

        :raises SmartPlugException: on error
        """

        self.system.relay_state = dict(state=1)

    def turn_off(self):
        """
        Turn the switch off.

        :raises SmartPlugException: on error
        """
        self.system.relay_state = dict(state=0)

    def toggle(self):
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    @property
    def led(self):
        """
        Returns the state of the led.

        :return: one of
                  instance.LED_STATE_ON
                  instance.LED_STATE_OFF
        :rtype: str
        """

        if not bool(self.system.led_off):
            return self.LED_STATE_ON
        else:
            return self.LED_STATE_OFF

    @led.setter
    def led(self, flag):
        """
        Sets the state of the led (night mode)

        :param str flag: one of
                  instance.LED_STATE_ON
                  instance.LED_STATE_OFF
        :raises SmartPlugException: on error
        """

        flag = str(flag)

        if flag in ('0', self.LED_STATE_OFF):
            self.system.led_off = dict(off=1)
        elif flag in ('1', self.LED_STATE_ON):
            self.system.led_off = dict(off=0)
        else:
            raise ValueError("State %s is not valid.", flag)

    @property
    def on_since(self):
        """
        Returns on-time

        :return: datetime for on since
        :rtype: datetime
        """
        return self.system.on_time

    @property
    def type(self):
        return self.system.mic_type


class HS200(SmartSwitch):
    pass


