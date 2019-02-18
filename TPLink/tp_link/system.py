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


class SysInfo(object):

    def __init__(self, device):
        self.device = device

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        data = self.device.query(system=dict(get_sysinfo=None))
        if data is not None and item in data:
            return data[item]

        raise AttributeError


class System(object):

    def __init__(self, device):
        object.__setattr__(self, 'device', device)
        self._sys_info = SysInfo(device)

    @property
    def sys_info(self):
        return self._sys_info

    def _send(self, **kwargs):
        return self.device.query(system=kwargs)

    def reboot(self, delay):
        self._send(reboot=dict(delay=delay))

    def reset(self, delay):
        self._send(reset=dict(delay=delay))

    def check_uboot(self):
        self._send(test_check_uboot=None)

    def check_config(self):
        self._send(check_new_config=None)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        value = getattr(self.sys_info, item, None)
        if value is not None:
            return value
        try:
            kwargs = {'get_' + item: dict()}
            return self._send(**kwargs)
        except:
            pass

        raise AttributeError(item)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            try:
                kwargs = {'set_' + key: value}
                self._send(**kwargs)
            except:
                try:
                    kwargs = {key: value}
                    self._send(**kwargs)
                except:
                    raise KeyError(key)
'''
{
    "get_sysinfo":{
        'err_code':0,
        'sw_ver':"1.1.0 Build 160521 Rel.085826",
        'hw_ver':"1.0",
        'model':    "HS200(US)",
        'mac':      "50:C7:BF:EC:B5:BE",
        'mic_mac': '50C7BF3393F1',
        'deviceId': "80067D896AAE9E6355F75961C15D7D3318D01055",
        'hwId':     "A0E3CC8F5C1166B27A16D56BE262A6D3",
        'mic_type':"IOT.SMARTPLUGSWITCH",
        'type': 'IOT.SMARTPLUGSWITCH',
        'fwId':"DB4F3246CD85AA59CAE738A63E7B9C34",
        'dev_name':"Wi-Fi Smart Light Switch",
        'icon_hash': "",
        'oemId':"4AFE44A41F868FD2340E6D1308D8551D",
        'alias':"Test Switch",
        'relay_state':0,
        'on_time':0,
        'active_mode':"none",
        'feature':"TIM",
        'updating':0,
        'rssi':-62,
        'led_off':0,
        'latitude':39.585187,
        'longitude':-105.363330,
        'ctrl_protocols': {
            'name': u'Linkie',
            'version': u'1.0'
        },
        'description': u'Smart Wi-Fi LED Bulb with Dimmable Light',
        'dev_state': u'normal',
        'disco_ver': u'1.0',
        'heapsize': 340808,
        'is_color': 0,
        'is_dimmable': 1,
        'is_factory': False,
        'is_variable_color_temp': 0,
        'light_state': {
            'dft_on_state': {
                'brightness': 50,
                'color_temp': 2700,
                'hue': 0,
                'mode': u'normal',
                'saturation': 0
            },
            'on_off': 0
        },
        'preferred_state': [
            {
                'brightness': 100,
                'color_temp': 2700,
                'hue': 0,
                'index': 0,
                'saturation': 0
            },
            {
                'brightness': 75,
                'color_temp': 2700,
                'hue': 0,
                'index': 1,
                'saturation': 0
            },
            {
                'brightness': 25,
                'color_temp': 2700,
                'hue': 0,
                'index': 2,
                'saturation': 0
            },
            {
                'brightness': 1,
                'color_temp': 2700,
                'hue': 0,
                'index': 3,
                'saturation': 0
            }
        ],
    }
}
'''
