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

import colorsys
import protocol
import emeter
from smartdevice import SmartDeviceBase

# model    color  colortemp   dimmable  e-meter
# LB100    False    False       True     False
# LB110    False    False       True     True
# LB120    False    True        True     True
# LB130    True     True        True     False

# LB100_US = {
#     u'sys_info': {
#         u'emeter': {
#             u'err_code': -2001,
#             u'err_msg': u'Module not support'
#         },
#         u'system': {
#             u'get_sysinfo': {
#                 u'active_mode': u'none',
#                 u'alias': u'New Light',
#                 u'ctrl_protocols': {
#                     u'name': u'Linkie',
#                     u'version': u'1.0'
#                 },
#                 u'description': u'Smart Wi-Fi LED Bulb with Dimmable Light',
#                 u'dev_state': u'normal',
#                 u'deviceId': u'8012996ED1F8DA43EFFD58B62BEC5ADE18192F88',
#                 u'disco_ver': u'1.0',
#                 u'err_code': 0,
#                 u'heapsize': 340808,
#                 u'hwId': u'111E35908497A05512E259BB76801E10',
#                 u'hw_ver': u'1.0',
#                 u'is_color': 0,
#                 u'is_dimmable': 1,
#                 u'is_factory': False,
#                 u'is_variable_color_temp': 0,
#                 u'light_state': {
#                     u'dft_on_state': {
#                         u'brightness': 50,
#                         u'color_temp': 2700,
#                         u'hue': 0,
#                         u'mode': u'normal',
#                         u'saturation': 0
#                     },
#                     u'on_off': 0
#                 },
#                 u'mic_mac': u'50C7BF3393F1',
#                 u'mic_type': u'IOT.SMARTBULB',
#                 u'model': u'LB100(US)',
#                 u'oemId': u'264E4E97B2D2B086F289AC1F00B90679',
#                 u'preferred_state': [
#                     {
#                         u'brightness': 100,
#                         u'color_temp': 2700,
#                         u'hue': 0,
#                         u'index': 0,
#                         u'saturation': 0
#                     },
#                     {
#                         u'brightness': 75,
#                         u'color_temp': 2700,
#                         u'hue': 0,
#                         u'index': 1,
#                         u'saturation': 0
#                     },
#                     {
#                         u'brightness': 25,
#                         u'color_temp': 2700,
#                         u'hue': 0,
#                         u'index': 2,
#                         u'saturation': 0
#                     },
#                     {
#                         u'brightness': 1,
#                         u'color_temp': 2700,
#                         u'hue': 0,
#                         u'index': 3,
#                         u'saturation': 0
#                     }
#                 ],
#                 u'rssi': -54,
#                 u'sw_ver': u'1.2.3 Build 170123 Rel.100146'
#             }
#         }
#     }
# }


def hsv_to_rgb(hue, saturation, value):
    r, g, b = colorsys.hsv_to_rgb(
        ((hue * 100.0) / 360.0) / 100.0,
        saturation / 100.0,
        value / 100.0
    )
    rgb = (
        int(round(r * 255.0)),
        int(round(g * 255.0)),
        int(round(b * 255.0))
    )

    return rgb


def rgb_to_hsv(red, green, blue):
    h, s, v = colorsys.rgb_to_hsv(
        red / 255.0,
        green / 255.0,
        blue / 255.0
    )

    hsv = (
        int(round(((h * 100) * 360) / 100)),
        int(round(s * 100)),
        int(round(v * 100))
    )

    return hsv


class Color(object):

    @property
    def rgb(self):
        return hsv_to_rgb(*self.hsv)

    @rgb.setter
    def rgb(self, (red, green, blue)):
        self.hsv = rgb_to_hsv(red, green, blue)

    @property
    def hsv(self):
        """
        Returns the current HSV state of the bulb, if supported

        :return: tuple containing current hue, saturation and value (0-255)
        :rtype: tuple
        """

        light_state = self._light_state
        if light_state['on_off'] == 0:
            hue = light_state['dft_on_state']['hue']
            saturation = light_state['dft_on_state']['saturation']
            value = light_state['dft_on_state']['brightness']
        else:
            hue = light_state['hue']
            saturation = light_state['saturation']
            value = light_state['brightness']
        hsv = (
            int((hue * 359) / 255),
            saturation,
            int((value * 255) / 100)
        )
        return hsv

    @hsv.setter
    def hsv(self, (hue, saturation, value)):
        """
        Sets new HSV, if supported

        :param int hue: hue 0-360
        :param int saturation: saturation 0-100
        :param int value: value, 0-100
        """
        self._light_state = dict(
            hue=int((hue * 255.0) / 359.0),
            saturation=int((saturation * 255.0) / 100.0),
            brightness=int(value),
            color_temp=0
        )


class ColorTemp(object):

    @property
    def color_temp(self):
        """
        Color temperature of the device, if supported

        :return: Color temperature in Kelvin
        :rtype: int
        """

        light_state = self._light_state
        if light_state['on_off'] == 0:
            return light_state['dft_on_state']['color_temp']
        else:
            return light_state['color_temp']

    @color_temp.setter
    def color_temp(self, temp):
        """
        Set the color temperature of the device, if supported

        :param int temp: The new color temperature, in Kelvin
        """
        self._light_state = dict(color_temp=temp)


class Brightness(object):

    @property
    def brightness(self):
        """
        Current brightness of the device, if supported

        :return: brightness in percent
        :rtype: int
        """
        light_state = self._light_state
        if light_state['on_off'] == 0:
            return light_state['dft_on_state']['brightness']
        else:
            return light_state['brightness']

    @brightness.setter
    def brightness(self, brightness):
        """
        Set the current brightness of the device, if supported

        :param int brightness: brightness in percent
        """

        self._light_state = dict(brightness=brightness)


class SmartBulb(SmartDeviceBase):
    """Representation of a TP-Link Smart Bulb.

    Usage example when used as library:
    p = SmartBulb("192.168.1.105")
    # print the devices alias
    print(p.alias)
    # change state of bulb
    p.state = "ON"
    p.state = "OFF"
    # query and print current state of plug
    print(p.state)
    # check whether the bulb supports color changes
    if p.is_color:
    # set the color to an HSV tuple
    p.hsv = (100, 0, 255)
    # get the current HSV value
    print(p.hsv)
    # check whether the bulb supports setting color temperature
    if p.is_variable_color_temp:
    # set the color temperature in Kelvin
    p.color_temp = 3000
    # get the current color temperature
    print(p.color_temp)
    # check whether the bulb is dimmable
    if p.is_dimmable:
    # set the bulb to 50% brightness
    p.brightness = 50
    # check the current brightness
    print(p.brightness)

    Errors reported by the device are raised as SmartPlugExceptions,
    and should be handled by the user of the library.

    """
    # bulb states
    BULB_STATE_ON = 'ON'
    BULB_STATE_OFF = 'OFF'
    Color = Color
    ColorTemp = ColorTemp
    Brightness = Brightness

    def _send(self, **kwargs):
        self.query(lightingservice=kwargs)

    @property
    def _light_state(self):
        return self._send(get_light_state=dict())

    @_light_state.setter
    def _light_state(self, state):
        self._send(transition_light_state=state)

    @property
    def mac(self):
        """
        Returns mac address

        :return: mac address in hexadecimal with colons, e.g. 01:23:45:67:89:ab
        :rtype: str
        """

        mac = self.system.mic_mac

        if ':' not in mac:
            mac = ':'.join(a + b for a, b in zip(mac, mac))
        return mac.upper()

    @property
    def is_color(self):
        """
        Whether the bulb supports color changes

        :return: True if the bulb supports color changes, False otherwise
        :rtype: bool
        """
        return isinstance(self, Color)

    @property
    def is_variable_color_temp(self):
        """
        Whether the bulb supports color temperature changes

        :return: True if the bulb supports color temperature changes, False
        otherwise
        :rtype: bool
        """
        return isinstance(self, ColorTemp)

    @property
    def is_dimmable(self):
        """
        Whether the bulb supports brightness changes

        :return: True if the bulb supports brightness changes, False otherwise
        :rtype: bool
        """
        return isinstance(self, Brightness)

    @property
    def state(self):
        """
        Retrieve the bulb state

        :returns: one of
                  BULB_STATE_ON
                  BULB_STATE_OFF
        :rtype: str
        """

        return (
            self.BULB_STATE_ON
            if self._light_state['on_off']
            else self.BULB_STATE_OFF
        )

    @state.setter
    def state(self, flag):
        """
        Set the new bulb state

        :param flag: one of
                           instance.BULB_STATE_ON
                           instance.BULB_STATE_OFF
        """

        flag = str(flag)

        if flag in ('1', self.BULB_STATE_ON):
            self._light_state = dict(on_off=1)
        elif flag in ('0', self.BULB_STATE_OFF):
            self._light_state = dict(on_off=0)
        else:
            raise ValueError("State %s is not valid.", flag)

    @property
    def is_on(self):
        """
        Returns whether device is on.

        :return: True if device is on, False otherwise
        """
        return self.state == self.BULB_STATE_ON

    @property
    def is_off(self):
        """
        Returns whether device is off.

        :return: True if device is off, False otherwise.
         :rtype: bool
        """
        return self.state == self.BULB_STATE_OFF

    def turn_on(self):
        """
        Turn the switch on.

        :raises SmartPlugException: on error
        """

        self.state = self.BULB_STATE_ON

    def turn_off(self):
        """
        Turn the switch off.

        :raises SmartPlugException: on error
        """
        self.state = self.BULB_STATE_OFF

    def toggle(self):
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    @property
    def type(self):
        return self.system.mic_type


class LB100(SmartBulb, Brightness):

    def __init__(self, ip, id):
        SmartBulb.__init__(self, ip, id)
        Brightness.__init__(self)


class LB110(SmartBulb, Brightness, emeter.EMeter):

    def __init__(self, ip, id):
        SmartBulb.__init__(self, ip, id)
        Brightness.__init__(self)
        emeter.EMeter.__init__(self, '_wh')


class LB120(SmartBulb, Brightness, emeter.EMeter, ColorTemp):

    def __init__(self, ip, id):
        SmartBulb.__init__(self, ip, id)
        Brightness.__init__(self)
        ColorTemp.__init__(self)
        emeter.EMeter.__init__(self, '_wh')


class LB130(SmartBulb, Brightness, ColorTemp, Color):

    def __init__(self, ip, id):
        SmartBulb.__init__(self, ip, id)
        Brightness.__init__(self)
        ColorTemp.__init__(self)
        Color.__init__(self)
