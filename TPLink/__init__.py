# -*- coding: utf-8 -*-
# super_class_updated
#
# This file is part of EventGhost.
# Copyright Â© 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

from __future__ import division
import eg


eg.RegisterPlugin(
    name='TPLink',
    author='K & Flyingsubs',
    version='2.6.1b',
    description=(
        'Controls TPLink Smart Plugs, Bulbs and Switches.'
    ),
    kind='external',
    help=(
        'Interval: The time in seconds between device updates. The smaller'
        'the value the more CPU time will be taken up but the faster you '
        'will receive device change events.\n\n'
        'Event Prefix: The beginning bits of the event.'
    )
    ,
    url=(
        'http://www.eventghost.net/forum/viewtopic.php?'
        'f=2&t=9648&p=45639#p45639'
    ),
    canMultiLoad=False,
    createMacrosOnAdd=False,
    guid='{C04FA578-9501-4354-B9CB-38FA487FF268}'
)

import color_chooser # NOQA
import threading # NOQA
import wx # NOQA
import colorsys # NOQA
import tp_link # NOQA
import wx.calendar # NOQA
from wx.lib.agw import peakmeter # NOQA
from datetime import datetime # NOQA

INTERVALS = (
    ('weeks', 604800),
    ('days', 86400),
    ('hours', 3600),
    ('minutes', 60),
    ('seconds', 1),
)


print_indent = ''


def find_differences(new, old):
    events = []

    for new_key, new_value in new.items():
        if new_key in old:
            old_value = old[new_key]
            if new_value != old_value:
                if (
                    isinstance(old_value, dict) and
                    isinstance(new_value, dict)
                ):
                    events += list(
                        new_key + event
                        for event in find_differences(new_value, old_value)
                    )


class PollThread(threading.Thread):

    def __init__(self, plugin, interval):
        self.plugin = plugin
        self.event = threading.Event()
        self.interval = interval
        threading.Thread.__init__(self, name='TPLink')
        self.daemon = True

    def stop(self):
        self.event.set()
        self.join(4)

    def run(self):
        """
        [
            {
                 'ip': '192.168.1.132',
                 'port': 9999,
                  'sys_info': {
                    'emeter': {
                        'err_msg': 'module not support',
                        'err_code': -1
                    },


                    ['system']['fwId']
                    ['system']['sw_ver']
                    ['system']['relay_state']
                    ['system']['led_off']
                    ['system']['alias']
                    ['system']['active_mode']
                    ['system']['latitude']
                    ['system']['longitude']

                    'system': {
                        'get_sysinfo': {
                            'oemId': '4AFE44A41F868FD2340E6D1308D8551D',
                            'mic_type': 'IOT.SMARTPLUGSWITCH',
                            'dev_name': 'Wi-Fi Smart Light Switch',
                            'on_time': 0,
                            'feature': 'TIM',
                            'fwId': 'DB4F3246CD85AA59CAE738A63E7B9C34',
                            'icon_hash': '',
                            'relay_state': 0,
                            'latitude': 39.585243,
                            'hw_ver': '1.0',
                            'led_off': 0,
                            'hwId': 'A0E3CC8F5C1166B27A16D56BE262A6D3',
                            'sw_ver': '1.1.0 Build 160521 Rel.085826',
                            'mac': '50:C7:BF:EC:B5:BE',
                            'active_mode': 'schedule',
                            'deviceId': '80067D896AAE9E6355F75961C15D7D3318D01055',
                            'updating': 0,
                            'longitude': -105.363457,
                            'alias': 'Test Switch',
                            'rssi': -57,
                            'model': 'HS200(US)',
                            'err_code': 0
                        }
                    },
                    'schedule': {
                        'get_rules': {
                            'rule_list': [
                                {
                                    'etime_opt': -1,
                                    'enable': 1,
                                    'name': '',
                                    'emin': 0,
                                    'eact': -1,
                                    'month': 0,
                                    'sact': 1,
                                    'repeat': 1,
                                    'smin': 24,
                                    'year': 0,
                                    'wday': [0, 1, 0, 0, 0, 0, 0],
                                    'id': '6EAC0129E3FB860F9E94E3F9C6EA8E46',
                                    'day': 0,
                                    'stime_opt': 0
                                }
                            ],
                            'enable': 1,
                            'err_code': 0
                        }
                    },
                    'cnCloud': {
                    'username'
                    'binded'
                    'fwDlPage'
                    'server'
                    'cld_connection'
                        'get_info': {
                            'username': '',
                            'tcspInfo': '',
                            'binded': 0,
                            'illegalType': -1,
                            'tcspStatus': -1,
                            'fwDlPage': '',
                            'server': 'devs.tplinkcloud.com',
                            'stopConnect': -1,
                            'fwNotifyType': 0,
                            'cld_connection': 0,
                            'err_code': 0
                        }
                    },
                    'count_down': {
                        'get_rules': {
                            'rule_list': [
                                {
                                    'delay': 0,
                                    'act': 1,
                                    'enable': 0,
                                    'id': '19F27821AD48EC9CF0FDE926211176B3',
                                    'name': 'add timer'
                                }
                            ],
                            'err_code': 0
                        }
                    },
                    'smartlife.iot.smartbulb.lightingservice': {
                        'err_msg': 'module not support',
                        'err_code': -1
                    },
                    'time': {
                        'get_time': {
                            'mday': 29,
                            'hor': 22,
                            'min': 8,
                            'month': 6,
                            'sec': 31,
                            'year': 2018,
                            'wday': 5,
                            'err_code': 0
                        },
                        'get_timezone': {
                            'index': 10,
                            'dst_offset': 60,
                            'tz_str': 'MST7MDT,M3.2.0,M11.1.0',
                            'zone_str': '(UTC-07:00) Mountain Daylight Time (US & Canada)',
                            'err_code': 0
                        }
                    },
                    'anti_theft': {
                        'get_rules': {
                            'rule_list': [
                                {
                                    'etime_opt': 0,
                                    'enable': 1,
                                    'name': '',
                                    'emin': 504,
                                    'day': 0,
                                    'month': 0,
                                    'frequency': 5,
                                    'smin': 457,
                                    'year': 0,
                                    'wday': [1, 0, 0, 0, 0, 0, 0],
                                    'id': 'D2E7502EAA0CFB64A38318887F208CE9',
                                    'repeat': 1,
                                    'stime_opt': 0
                                }
                            ],
                            'enable': 1,
                            'err_code': 0
                        }
                    }
                }
            }
        ]
        :return:
        """
        old_devices = tp_link.discover()

        for i, device in enumerate(old_devices[:]):
            del device['sys_info']['time']['get_time']
            sys_info = device.pop('sys_info')
            device.update(sys_info)
            old_devices[i] = device

        for device in tp_link.smart_switches:

            data = dict(
                alias=device.alias,
                state=device.state,
                location=device.latitude_longitude,
                id=device.id,
                led=device.led,
                ip=device.ip
            )
            devices['switches'] += [data]

        for device in tp_link.smart_plugs:
            data = dict(
                alias=device.alias,
                state=device.state,
                location=device.latitude_longitude,
                id=device.id,
                led=device.led,
                ip=device.ip
            )
            devices['plugs'] += [data]

        for device in tp_link.smart_bulbs:
            data = dict(
                alias=device.alias,
                state=device.state,
                location=device.latitude_longitude,
                id=device.id,
                ip=device.ip,
                hsv=getattr(device, 'hsv', None),
                color_temp=getattr(device, 'color_temp', None),
                brightness=getattr(device, 'brightness', None)
            )

            devices['bulbs'] += [data]

        while not self.event.isSet():
            tp_link.discover()

            for data in devices['switches']:
                if data['id'] not in tp_link.smart_switches:
                    self.plugin.TriggerEvent(
                        'SmartSwitch.{0}.Removed'.format(data['alias'])
                    )
                    devices['switches'].remove(data)

                else:
                    device = tp_link.smart_switches[data['id']]
                    ip = device.ip
                    alias = device.alias
                    state = device.state
                    location = device.latitude_longitude
                    led = device.led

                    if alias != data['alias']:

                        self.plugin.TriggerEvent(
                            'SmartSwitch.{0}.Alias'.format(data['alias']),
                            alias
                        )
                        data['alias'] = alias

                    if ip != data['ip']:
                        data['ip'] = ip
                        self.plugin.TriggerEvent(
                            'SmartSwitch.{0}.IP'.format(alias),
                            ip
                        )

                    if state != data['state']:
                        data['state'] = state
                        self.plugin.TriggerEvent(
                            'SmartSwitch.{0}.State.{1}'.format(
                                alias,
                                state.title()
                            )
                        )

                    if location != data['location']:
                        data['location'] = location
                        self.plugin.TriggerEvent(
                            'SmartSwitch.{0}.Location'.format(alias),
                            location
                        )

                    if led != data['led']:
                        data['led'] = led
                        self.plugin.TriggerEvent(
                            'SmartSwitch.{0}.Led.{1}'.format(
                                alias,
                                led.title()
                            )
                        )

            for data in devices['plugs']:
                if data['id'] not in tp_link.smart_plugs:
                    self.plugin.TriggerEvent(
                        'SmartPlug.{0}.Removed'.format(data['alias'])
                    )
                    devices['plugs'].remove(data)

                else:
                    device = tp_link.smart_plugs[data['id']]
                    ip = device.ip
                    alias = device.alias
                    state = device.state
                    location = device.latitude_longitude
                    led = device.led

                    if alias != data['alias']:
                        self.plugin.TriggerEvent(
                            'SmartPlug.{0}.Alias'.format(data['alias']),
                            alias
                        )
                        data['alias'] = alias

                    if ip != data['ip']:
                        data['ip'] = ip
                        self.plugin.TriggerEvent(
                            'SmartPlug.{0}.IP'.format(alias),
                            ip
                        )

                    if state != data['state']:
                        data['state'] = state
                        self.plugin.TriggerEvent(
                            'SmartPlug.{0}.State.{1}'.format(
                                alias,
                                state.title()
                            )
                        )

                    if location != data['location']:
                        data['location'] = location
                        self.plugin.TriggerEvent(
                            'SmartPlug.{0}.Location'.format(alias),
                            location
                        )

                    if led != data['led']:
                        data['led'] = led
                        self.plugin.TriggerEvent(
                            'SmartPlug.{0}.Led.{1}'.format(
                                alias,
                                led.title()
                            )
                        )

            for data in devices['bulbs']:
                if data['id'] not in tp_link.smart_bulbs:
                    self.plugin.TriggerEvent(
                        'SmartBulb.{0}.Removed'.format(data['alias'])
                    )
                    devices['bulbs'].remove(data)

                else:
                    device = tp_link.smart_bulbs[data['id']]
                    ip = device.ip
                    alias = device.alias
                    state = device.state
                    location = device.latitude_longitude

                    hsv = getattr(device, 'hsv', None)
                    color_temp = getattr(device, 'color_temp', None)
                    brightness = getattr(device, 'brightness', None)

                    if alias != data['alias']:
                        self.plugin.TriggerEvent(
                            'SmartBulb.{0}.Alias'.format(data['alias']),
                            alias
                        )
                        data['alias'] = alias

                    if ip != data['ip']:
                        data['ip'] = ip
                        self.plugin.TriggerEvent(
                            'SmartBulb.{0}.IP'.format(alias),
                            ip
                        )

                    if state != data['state']:
                        data['state'] = state
                        self.plugin.TriggerEvent(
                            'SmartBulb.{0}.State.{1}'.format(
                                alias,
                                state.title()
                            )
                        )

                    if location != data['location']:
                        data['location'] = location
                        self.plugin.TriggerEvent(
                            'SmartBulb.{0}.Location'.format(alias),
                            location
                        )

                    if hsv != data['hsv']:
                        data['hsv'] = hsv
                        self.plugin.TriggerEvent(
                            'SmartBulb.{0}.Color'.format(alias),
                            hsv
                        )

                    if color_temp != data['color_temp']:
                        data['color_temp'] = color_temp
                        self.plugin.TriggerEvent(
                            'SmartBulb.{0}.ColorTemp'.format(alias),
                            color_temp
                        )

                    if brightness != data['brightness']:
                        data['brightness'] = brightness
                        self.plugin.TriggerEvent(
                            'SmartBulb.{0}.Brightness'.format(alias),
                            brightness
                        )

            for device in tp_link.smart_switches:
                for data in devices['switches']:
                    if data['id'] == device.id:
                        break
                else:
                    data = dict(
                        alias=device.alias,
                        state=device.state,
                        location=device.location,
                        id=device.id,
                        led=device.led,
                        ip=device.ip
                    )
                    devices['switches'] += [data]
                    self.plugin.TriggerEvent(
                        'SmartSwitch.{0}.Added'.format(data['alias'])
                    )

            for device in tp_link.smart_plugs:
                for data in devices['plugs']:
                    if data['id'] == device.id:
                        break
                else:
                    data = dict(
                        alias=device.alias,
                        state=device.state,
                        location=device.location,
                        id=device.id,
                        led=device.led,
                        ip=device.ip
                    )
                    devices['switches'] += [data]
                    self.plugin.TriggerEvent(
                        'SmartPlug.{0}.Added'.format(data['alias'])
                    )

            for device in tp_link.smart_bulbs:
                for data in devices['bulbs']:
                    if data['id'] == device.id:
                        break
                else:
                    data = dict(
                        alias=device.alias,
                        state=device.state,
                        location=device.location,
                        id=device.id,
                        ip=device.ip,
                        hsv=getattr(device, 'hsv', None),
                        color_temp=getattr(device, 'color_temp', None),
                        brightness=getattr(device, 'brightness', None)
                    )
                    devices['bulbs'] += [data]
                    self.plugin.TriggerEvent(
                        'SmartBulb.{0}.Added'.format(data['alias'])
                    )

            self.event.wait(self.interval)


class TPLink(eg.PluginBase):

    def __init__(self):
        super(TPLink, self).__init__()
        self.devices = {}
        self.thread = None

        self.AddAction(SwitchState)
        self.AddAction(SwitchLED)
        self.AddAction(SwitchToggle)
        self.AddAction(PlugState)
        self.AddAction(PlugLED)
        self.AddAction(PlugToggle)
        self.AddAction(BulbState)
        self.AddAction(BulbToggle)
        self.AddAction(BulbColor)
        self.AddAction(BulbColorTemp)
        self.AddAction(BulbDimLevel)
        self.AddAction(Schedule)
        self.AddAction(GetMeter)
        self.AddAction(ClearEMeter)
        self.AddAction(ResetDevice)
        self.AddAction(TestUBoot)
        self.AddAction(RebootDevice)
        self.AddAction(FlashFirmware)
        self.AddAction(CloudServer)
        self.AddAction(SetLocation)
        self.AddAction(ChangeAlias)
        self.AddAction(EMeterCalibration)
        self.AddAction(ChangeEMeterGains)
        self.AddAction(GetDevice, hidden=True)

    def __start__(self, prefix='TPLink', interval=0.5, port=9999):
        self.info.eventPrefix = prefix
        while self.thread is not None:
            pass
        self.thread = PollThread(self, interval)
        self.thread.start()

    def __stop__(self):
        if self.thread is not None:
            self.thread.stop()
            self.thread = None

    def __close__(self):
        pass

    def Configure(self, prefix='TPLink', interval=0.5, port=9999):
        panel = eg.ConfigPanel()
        prefix_st = panel.StaticText('Event Prefix:')
        interval_st = panel.StaticText('Poll Interval:')

        prefix_ctrl = panel.TextCtrl(prefix)
        interval_ctrl = panel.SpinNumCtrl(
            interval,
            min=0.1,
            max=60.0,
            increment=0.1
        )

        def add_ctrl(st, widget):
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(st, 0, wx.EXPAND | wx.ALL, 5)
            sizer.Add(widget, 0, wx.EXPAND | wx.ALL, 5)
            panel.sizer.Add(sizer)

        add_ctrl(prefix_st, prefix_ctrl)
        add_ctrl(interval_st, interval_ctrl)

        while panel.Affirmed():
            panel.SetResult(
                prefix_ctrl.GetValue(),
                interval_ctrl.GetValue()
            )


class DevicePanel(wx.Panel):

    def __init__(self, parent, device_id, func):

        devices = list(device for device in tp_link if func(device))
        wx.Panel.__init__(self, parent)
        colour_image = wx.EmptyImage(30, 20)

        name_ctrl = wx.StaticText(self, -1, 'Device Name: ')
        model_ctrl = wx.StaticText(self, -1, 'Model: ')
        type_ctrl = wx.StaticText(self, -1, 'Type: ')
        ip_ctrl = wx.StaticText(self, -1, 'IP Address: ')
        mac_ctrl = wx.StaticText(self, -1, 'MAC Address: ')

        time_ctrl = wx.StaticText(self, -1, 'Time: ')
        tzone_ctrl = wx.StaticText(self, -1, 'Time Zone: ')
        loc_ctrl = wx.StaticText(self, -1, 'Location: ')

        softver_ctrl = wx.StaticText(self, -1, 'Firmware Version: ')
        hardver_ctrl = wx.StaticText(self, -1, 'Hardware Version: ')
        softid_ctrl = wx.StaticText(self, -1, 'Firmware Id: ')
        hardid_ctrl = wx.StaticText(self, -1, 'Hardware Id: ')
        oemid_ctrl = wx.StaticText(self, -1, 'OEM Id: ')
        update_ctrl = wx.StaticText(self, -1, 'Updating Firmware:')

        state_ctrl = wx.StaticText(self, -1, 'State: ')
        mode_ctrl = wx.StaticText(self, -1, 'Active Mode: ')
        watts_ctrl = wx.StaticText(self, -1, 'Watts: N/A')
        vgain_ctrl = wx.StaticText(self, -1, 'V Gain: ')
        igain_ctrl = wx.StaticText(self, -1, 'I Gain: ')

        opt1_ctrl = wx.StaticText(self, -1, '')
        opt2_ctrl = wx.StaticText(self, -1, '')
        opt3_ctrl = wx.StaticText(self, -1, '')

        colour_btn = wx.StaticBitmap(
            self,
            -1,
            colour_image.ConvertToBitmap(),
            size=(30, 20)
        )
        colour_btn.Hide()

        meter_st = wx.StaticText(self, -1, 'Signal Strength:')
        meter_suf = wx.StaticText(self, -1, '-- dBm')
        meter_ctrl = peakmeter.PeakMeterCtrl(
            self,
            -1,
            size=(150, 15),
            style=wx.BORDER_SUNKEN,
            agwStyle=peakmeter.PM_HORIZONTAL
        )

        meter_ctrl.SetMeterBands(1, 20)
        meter_ctrl.SetFalloffEffect(False)
        meter_ctrl.ShowGrid(False)
        meter_ctrl.SetRangeValue(20, 40, 100)
        meter_ctrl.SetData([0], 0, 1)

        choices = (
            sorted(
                list(
                    (device.alias, device.id) for device in devices
                )
            )
        )

        device_st = wx.StaticText(self, -1, 'Device:')
        device_ctrl = wx.Choice(
            self,
            -1,
            choices=list(device[0] for device in choices)
        )

        def SetData():
            dev_id = choices[device_ctrl.GetSelection()][1]

            for device in devices:
                if dev_id == device.id:
                    break
            else:
                return

            location = device.location
            loc_ctrl.SetLabel(
                'Location: {0} ({1}, {2})'.format(
                    geocoding.get_location(*location),
                    *location
                )
            )

            try:
                time_zone = device.time.timezone
                if 'zone_str' in time_zone:
                    time_zone = time_zone['zone_str']
                else:
                    time_zone = 'N/A'

                tzone_ctrl.SetLabel('Time Zone: ' + time_zone)

            except tp_link.NotSupportedError:
                tzone_ctrl.SetLabel('Time Zone: NOT SUPPORTED')

            try:
                time_ctrl.SetLabel('Time: ' + str(device.time))
            except tp_link.NotSupportedError:
                time_ctrl.SetLabel('Time: NOT SUPPORTED')

            type_ctrl.SetLabel('Type: ' + device.type)
            name_ctrl.SetLabel('Device Name: ' + device.alias)
            softid_ctrl.SetLabel('Firmware Id: ' + device.firmware.id)
            hardid_ctrl.SetLabel('Hardware Id: ' + device.hardware.id)
            oemid_ctrl.SetLabel('OEM Id: ' + device.oem_id)

            update_ctrl.SetLabel(
                'Updating Firmware: ' + str(bool(device.firmware.updating))
            )
            state_ctrl.SetLabel('State: ' + device.state.title())
            mode_ctrl.SetLabel('Active Mode: ' + device.active_mode)

            if device.has_emeter:
                gains = device.e_meter.emeter_gain
                vgain = gains['vgain']
                igain = gains['igain']
                watts = device.e_meter.current_consumption
            else:
                vgain = 'N/A'
                igain = 'N/A'
                watts = 'N/A'

            vgain_ctrl.SetLabel(
                'V Gain: ' + str(vgain)
            )
            igain_ctrl.SetLabel(
                'I Gain: ' + str(igain)
            )
            watts_ctrl.SetLabel(
                'Watts: ' + str(watts)
            )
            ip_ctrl.SetLabel(
                'IP Address: ' + device.ip
            )
            mac_ctrl.SetLabel(
                'MAC Address: ' + device.mac
            )
            model_ctrl.SetLabel(
                'Model: ' + device.model
            )
            softver_ctrl.SetLabel(
                'Firmware Version: ' + device.firmware.version
            )
            hardver_ctrl.SetLabel(
                'Hardware Version: ' + device.hardware.version
            )

            dBm = device.rssi

            if isinstance(device, tp_link.SmartBulb.Brightness):
                level = str(device.brightness) + '%'
                opt1_ctrl.SetLabel('Light Level: ' + level)
            elif isinstance(device, (tp_link.SmartSwitch, tp_link.SmartBulb)):
                opt1_ctrl.SetLabel('LED: ' + device.led.title())
            else:
                opt1_ctrl.SetLabel('')

            if isinstance(device, tp_link.SmartBulb.ColorTemp):
                temp = str(device.colour_temp) + ' kelvin'
                opt2_ctrl.SetLabel('Color Temp: ' + temp)
            else:
                opt2_ctrl.SetLabel('')

            if isinstance(device, tp_link.SmartBulb.Color):
                hsv = device.hsv
                h, s, v = hsv
                h = (h * 359) / 255
                s = (s * 100) / 255
                v = (v * 100) / 255

                r, g, b = colorsys.hsv_to_rgb(h, s / 100.0, v / 100.0)
                colour_image.SetRGBRect((1, 1, 30, 20), r, g, b)
                colour_btn.SetBitmap(colour_image.ConvertToBitmap())

                colour_btn.Show()
                opt3_ctrl.SetLabel('Color: ')

            elif isinstance(device, (tp_link.SmartSwitch, tp_link.SmartBulb)):
                def display_time(seconds):
                    result = []
                    for time_name, count in INTERVALS:
                        time_amount = seconds // count
                        seconds -= time_amount * count

                        if time_amount < 2:
                            time_name = time_name[:-1]

                        result.append(
                            "{} {}".format(time_amount, time_name)
                        )

                    return ', '.join(result)

                opt3_ctrl.SetLabel(
                    'On Time: ' + display_time(int(str(device.on_since)))
                )

            else:
                opt3_ctrl.SetLabel('')
                colour_btn.Hide()

            if dBm <= -100:
                quality = 0
            elif dBm >= -50:
                quality = 100
            else:
                quality = 2 * (dBm + 100)

            if quality <= 20:
                colour = wx.Colour(255, 0, 0)
            elif quality <= 40:
                colour = wx.Colour(255, 255, 0)
            else:
                colour = wx.Colour(0, 255, 0)
            meter_ctrl.SetBandsColour(colour, colour, colour)
            meter_ctrl.SetData([quality], 0, 1)
            meter_suf.SetLabel(str(dBm) + ' dBm')

        for i, dev in enumerate(choices):
            if device_id in dev:
                device_ctrl.SetSelection(i)
                SetData()
                break
        else:
            if choices:
                device_ctrl.SetSelection(0)
                SetData()

        sizer = wx.BoxSizer(wx.VERTICAL)
        data_box = wx.StaticBox(self, -1, 'Device Information')
        data_sizer = wx.StaticBoxSizer(data_box, wx.VERTICAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        center_sizer = wx.BoxSizer(wx.HORIZONTAL)
        meter_sizer = wx.BoxSizer(wx.HORIZONTAL)
        device_sizer = wx.BoxSizer(wx.HORIZONTAL)

        meter_sizer.Add(meter_st, 0, wx.ALL, 5)
        meter_sizer.Add(meter_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        meter_sizer.Add(meter_suf, 0, wx.ALL, 5)

        device_sizer.Add(device_st, 0, wx.EXPAND | wx.ALL, 5)
        device_sizer.Add(device_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        colour_sizer = wx.BoxSizer(wx.HORIZONTAL)
        colour_sizer.Add(opt3_ctrl, 0, wx.ALL, 5)
        colour_sizer.Add(colour_btn, 0, wx.EXPAND | wx.ALL, 5)

        left_sizer.Add(name_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        left_sizer.Add(model_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        left_sizer.Add(ip_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        left_sizer.Add(mac_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        left_sizer.Add(state_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        left_sizer.Add(opt1_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        right_sizer.Add(mode_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(type_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(watts_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(vgain_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(igain_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(opt2_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        center_sizer.Add(left_sizer)
        center_sizer.AddStretchSpacer()
        center_sizer.Add(right_sizer)
        center_sizer.AddStretchSpacer()

        data_sizer.Add(meter_sizer, 0, wx.EXPAND)
        data_sizer.Add(center_sizer, 0, wx.EXPAND)
        data_sizer.Add(colour_sizer, 0, wx.EXPAND)
        data_sizer.Add(loc_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        data_sizer.Add(time_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        data_sizer.AddSpacer(1)
        data_sizer.AddSpacer(1)
        data_sizer.Add(tzone_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        data_sizer.Add(softver_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        data_sizer.Add(softid_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        data_sizer.Add(hardver_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        data_sizer.Add(hardid_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        data_sizer.Add(oemid_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        data_sizer.Add(update_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        data_sizer.AddSpacer(1)
        data_sizer.AddSpacer(1)
        sizer.Add(data_sizer, 0, wx.EXPAND)
        sizer.Add(device_sizer)

        self.SetSizer(sizer)

        def OnChoice(evt):
            SetData()
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, OnChoice)

        def get_string_selection():
            return choices[device_ctrl.GetSelection()][1]

        self.GetStringSelection = get_string_selection


class SetLocation(eg.ActionBase):
    name = 'Set Device Location'
    description = 'Set the location of a device.'

    def GetLabel(
        self,
        device,
        address='',
        city='',
        state='',
        latitude=None,
        longitude=None
    ):
        if None not in (latitude, longitude):
            return (
                '%s: %s, (%f, %f)' % (self.name, device, latitude, longitude)
            )

        return (
            '%s: %s, %s %s %s' % (self.name, device, address, city, state)
        )

    def __call__(
        self,
        device,
        address='',
        city='',
        state='',
        latitude=None,
        longitude=None
    ):
        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, device.id):
                if None not in (latitude, longitude):
                    dvc.latitude_longitude = (latitude, longitude)
                else:
                    try:
                        dvc.geo_location = (address, city, state)
                    except RuntimeError:
                        eg.PrintError(
                            self.name + ': Google Geocoding API key not set'
                        )
                return True

        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return False

    def _check_device(self, _):
        return True

    def Configure(
        self,
        device='',
        address='',
        city='',
        state='',
        latitude=None,
        longitude=None
    ):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            device,
            self._check_device
        )

        address_st = panel.StaticText('Address:')
        address_ctrl = panel.TextCtrl(address)

        city_st = panel.StaticText('City:')
        city_ctrl = panel.TextCtrl(city)

        state_st = panel.StaticText('State/Province/Country:')
        state_ctrl = panel.TextCtrl(state)

        if latitude is None:
            latitude = ''
        else:
            latitude = str(latitude)

        if longitude is None:
            longitude = ''
        else:
            longitude = str(longitude)

        or_st = panel.StaticText('OR')

        latitude_st = panel.StaticText('Latitude:')
        latitude_ctrl = panel.TextCtrl(latitude)

        longitude_st = panel.StaticText('Longitude:')
        longitude_ctrl = panel.TextCtrl(longitude)

        def on_choice(evt):
            device_id = device_ctrl.GetStringSelection()
            for d in tp_link:
                if d.id == device_id:
                    try:
                        geolocation = d.geo_location.split(', ')
                        address_ctrl.SetValue(geolocation[0])
                        city_ctrl.SetValue(geolocation[1])
                        state_ctrl.SetValue(geolocation[2])
                    except RuntimeError:
                        eg.PrintError(
                            self.name + ': Google Geocoding API key not set'
                        )
                        address_ctrl.SetValue('')
                        city_ctrl.SetValue('')
                        state_ctrl.SetValue('')
                        address_ctrl.Enable(False)
                        city_ctrl.Enable(False)
                        state_ctrl.Enable(False)

                    lat, lng = d.latitude_longitude
                    latitude_ctrl.SetValue(str(lat))
                    longitude_ctrl.SetValue(str(lng))
                    break
            evt.Skip()
        device_ctrl.Bind(wx.EVT_CHOICE, on_choice)

        eg.EqualizeWidths(
            (address_st, city_st, state_st, latitude_st, longitude_st)
        )

        def add(st, ctrl):
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(st, 0, wx.EXPAND | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL, 5)
            panel.sizer.Add(sizer, 0, wx.EXPAND)

        panel.sizer.Add(device_ctrl)

        add(address_st, address_ctrl)
        add(city_st, city_ctrl)
        add(state_st, state_ctrl)

        or_sizer = wx.BoxSizer(wx.HORIZONTAL)
        or_sizer.AddStretchSpacer(1)
        or_sizer.Add(or_st)
        or_sizer.AddStretchSpacer(1)

        panel.sizer.Add(or_sizer, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)

        add(latitude_st, latitude_ctrl)
        add(longitude_st, longitude_ctrl)
        panel.sizer.AddSpacer(1)
        panel.sizer.AddSpacer(1)

        while panel.Affirmed():
            latitude = latitude_ctrl.GetValue()
            longitude = longitude_ctrl.GetValue()

            if latitude and longitude:
                latitude = float(latitude)
                longitude = float(longitude)

            else:
                latitude = None
                longitude = None

            panel.SetResult(
                device_ctrl.GetStringSelection(),
                address_ctrl.GetValue(),
                city_ctrl.GetValue(),
                state_ctrl.GetValue(),
                latitude,
                longitude

            )


class ToggleBase(eg.ActionBase):
    name = ''
    description = ''

    def __call__(self, device):
        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, dvc.id):
                if dvc.state.lower() == 'on':
                    dvc.state = 'OFF'
                else:
                    dvc.state = 'ON'
                return True

        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return False

    def _check_device(self, device):
        raise NotImplementedError

    def Configure(self, device=''):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            device,
            self._check_device
        )

        panel.sizer.Add(device_ctrl, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.GetStringSelection()
            )


class StateBase(eg.ActionBase):
    name = ''
    description = ''

    def GetLabel(self, device, state):

        if isinstance(state, (bool, int)):
            state = str(int(state))

        if state.isdigit():
            state = 'On' if state == '1' else 'Off'

        return '%s: %s %s' % (self.name, device, state)

    def __call__(self, device, state):
        if isinstance(state, (bool, int)):
            state = str(int(state))

        if state.isdigit():
            state = 'On' if state == '1' else 'Off'

        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, dvc.id):
                if self._check_device(dvc):
                    dvc.state = state.upper()
                    return True
                else:
                    eg.PrintNotice(
                        '%s: Device %s not proper type.' %
                        (self.name, device)
                    )
                    return False

        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return False

    def _check_device(self, device):
        raise NotImplementedError

    def Configure(self, device='', state='Off'):
        panel = eg.ConfigPanel()

        selection = 0 if state == 'Off' else 1

        device_ctrl = DevicePanel(
            panel,
            device,
            self._check_device
        )

        state_st = panel.StaticText('State:')
        state_ctrl = panel.Choice(value=selection, choices=['Off', 'On'])

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(state_st, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(state_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(device_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.GetStringSelection(),
                state_ctrl.GetStringSelection()
            )


class LEDBase(eg.ActionBase):
    name = ''
    description = ''

    def GetLabel(self, device, led):
        if isinstance(led, (bool, int)):
            led = str(int(led))

        if led.isdigit():
            led = 'On' if led == '1' else 'Off'

        return '%s: %s %s' % (self.name, device, led)

    def __call__(self, device, led):
        if isinstance(led, (int, bool)):
            led = 'ON' if led else 'OFF'

        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, dvc.id):
                if self._check_device(dvc):
                    dvc.led = led.upper()
                    return True

                eg.PrintNotice(
                    '%s: Device %s not proper type.' %
                    (self.name, device)
                )
                return False

        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return False

    def _check_device(self, device):
        raise NotImplementedError

    def Configure(self, device='', led=0):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            device,
            self._check_device
        )

        led_st = panel.StaticText('Led:')
        led_ctrl = panel.Choice(value=led, choices=['Off', 'On'])

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(led_st, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(led_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(device_ctrl)
        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.GetStringSelection(),
                led_ctrl.GetValue()
            )


class SwitchState(StateBase):
    name = 'Change Switch State'
    description = 'Turn switch on or off.'

    def _check_device(self, device):
        return isinstance(device, tp_link.SmartSwitch)


class SwitchLED(LEDBase):
    name = 'Change Switch LED'
    description = 'Change the LED state on a switch.'

    def _check_device(self, device):
        return isinstance(device, tp_link.SmartSwitch)


class SwitchToggle(ToggleBase):
    name = 'Toggle a Switch On or Off'
    description = 'Toggles a switch on or off'

    def _check_device(self, device):
        return isinstance(device, tp_link.SmartSwitch)


class PlugState(StateBase):
    name = 'Change Plug State'
    description = 'Turn plug on or off.'

    def _check_device(self, device):
        return isinstance(device, tp_link.SmartPlug)


class PlugLED(LEDBase):
    name = 'Change Plug LED'
    description = 'Change the LED state on a plug.'

    def _check_device(self, device):
        return isinstance(device, tp_link.SmartPlug)


class PlugToggle(ToggleBase):
    name = 'Toggle a Plug On or Off'
    description = 'Toggles a plug on or off'

    def _check_device(self, device):
        return isinstance(device, tp_link.SmartPlug)


class BulbState(StateBase):
    name = 'Change Bulb State'
    description = 'Turn bulb on or off.'

    def _check_device(self, device):
        return isinstance(device, tp_link.SmartBulb)


class BulbToggle(ToggleBase):
    name = 'Toggle a Bulb On or Off'
    description = 'Toggles a bulb on or off'

    def _check_device(self, device):
        return isinstance(device, tp_link.SmartBulb)


class BulbDimLevel(eg.ActionBase):
    name = 'Change Bulb Light Level'
    description = 'Change the light level of a bulb (if supported).'

    def GetLabel(self, device, level):
        if not isinstance(level, int) and level.isdigit():
            level = int(level)

        return '%s: %s %d%%' % (self.name, device, level)

    def __call__(self, device, level):
        if not isinstance(level, int) and level.isdigit():
            level = int(level)

        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, dvc.id):
                if self._check_device(dvc):
                    dvc.brightness = level
                    return True
                eg.PrintNotice(
                    '%s: Device %s not proper type.' %
                    (self.name, device)
                )
                return False

        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return False

    def _check_device(self, device):
        return isinstance(device, tp_link.SmartBulb) and device.is_dimmable

    def Configure(self, device='', level=0):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            device,
            self._check_device
        )

        level_st = panel.StaticText('Level:')
        level_ctrl = panel.SpinIntCtrl(level, min=0, max=100)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(level_st, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(level_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(device_ctrl)
        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.GetStringSelection(),
                level_ctrl.GetValue()
            )


class BulbColor(eg.ActionBase):
    name = 'Change Bulb Color'
    description = 'Change the color of a bulb (if supported).'

    def GetLabel(self, device, red, green, blue):

        return (
            '%s: %s Red: %d, Green: %d, Blue: %d' %
            (self.name, device, red, green, blue)
        )

    def __call__(self, device, red, green, blue):

        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, dvc.id):
                if self._check_device(dvc):
                    dvc.rgb = (red, green, blue)
                    return True

                eg.PrintNotice(
                    '%s: Device %s not proper type.' %
                    (self.name, device)
                )
                return False

        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return False

    def _check_device(self, device):
        return isinstance(device, tp_link.SmartBulb) and device.is_color

    def Configure(self, device='', red=150, green=30, blue=30):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            device,
            self._check_device
        )

        colour_ctrl = color_chooser.ColorChooser(
            panel,
            -1,
            value=(red, green, blue)
        )
        panel.sizer.Add(device_ctrl)
        panel.sizer.Add(colour_ctrl, 1, wx.ALL, 5)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.GetStringSelection(),
                *colour_ctrl.GetValue()
            )


class BulbColorTemp(eg.ActionBase):
    name = 'Change Bulb Color Temperature'
    description = 'Change the color temperature of a bulb (if supported).'

    def GetLabel(self, device, temp):
        if not isinstance(temp, int) and temp.isdigit():
            temp = int(temp)

        return '%s: %s %dk' % (self.name, device, temp)

    def __call__(self, device, temp):
        if not isinstance(temp, int) and temp.isdigit():
            temp = int(temp)

        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, dvc.id):
                if self._check_device(dvc):
                    dvc.color_temp = temp
                    return True
                eg.PrintNotice(
                    '%s: Device %s not proper type.' %
                    (self.name, device)
                )
                return False

        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return False

    def _check_device(self, device):
        return (
            isinstance(device, tp_link.SmartBulb) and
            device.is_variable_color_temp
        )

    def Configure(self, device='', temp=5500):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            device,
            self._check_device
        )

        temp_st = panel.StaticText('Color Temp:')
        temp_ctrl = panel.SpinIntCtrl(temp, min=2700, max=6500)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(temp_st, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(temp_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(device_ctrl)
        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.GetStringSelection(),
                temp_ctrl.GetValue()
            )


class GetMeter(eg.ActionBase):
    name = 'Get Meter Data'
    description = 'Get devices meter data (if supported).'

    def GetLabel(self, device, day=None, month=None, year=None, display=False):

        return (
            '%s: %s %s/%s/%s' %
            (self.name, device, str(day), str(month), str(year))
        )

    def __call__(self, device, day=None, month=None, year=None, display=False):
        if isinstance(day, datetime):
            year = day.year
            month = day.month
            day = day.day

        date = datetime.now()
        date = (date.day, date.month, date.year)

        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, dvc.id):
                if dvc.is_metered():
                    if (day, month, year) == date:
                        data = dvc.get_emeter_realtime()
                    elif month is not None and year is not None:
                        data = dvc.get_emeter_daily(month, year)
                    else:
                        data = dvc.get_emeter_monthly(year)

                    if display:
                        if day is not None:
                            print('%s: %s' % (day, data[day]))
                        else:
                            for key, value in data.items:
                                print('%s: %s' % (str(key), str(value)))
                    if day is not None:
                        return data[day]
                    return data

                eg.PrintNotice(
                    '%s: Device %s not proper type.' %
                    (self.name, device)
                )
                return False

        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return False

    def Configure(
        self,
        device='',
        day=None,
        month=None,
        year=None,
        display=False
    ):
        panel = eg.ConfigPanel()

        if day is None:
            day = datetime.today().day
        if month is None:
            month = datetime.today().month - 1
        if year is None:
            year = datetime.today().year

        device_ctrl = DevicePanel(
            panel,
            device,
            self._check_device
        )

        calendar_ctrl = wx.calendar.CalendarCtrl(
            panel,
            -1,
            wx.DateTimeFromDMY(day, month, year),
            style=(
                wx.calendar.CAL_SEQUENTIAL_MONTH_SELECTION |
                wx.calendar.CAL_SUNDAY_FIRST
            )
        )

        display_ctrl = wx.CheckBox(panel, -1, 'Print to log')
        display_ctrl.SetValue(display)

        def OnCalendar(evt):
            date = calendar_ctrl.GetDate()
            today = datetime.today()
            new_date = [date.GetDay(), date.GetMonth(), date.GetYear()]

            if date.GetYear() > today.year:
                new_date[2] = today.year
            if (
                date.GetMonth() > today.month - 1 and
                date.GetYear() == today.year
            ):
                new_date[1] = today.month - 1
            if (
                date.GetDay() > today.day and
                date.GetMonth() == today.month - 1
            ):
                new_date[0] = today.day

            if new_date != [date.GetDay(), date.GetMonth(), date.GetYear()]:
                calendar_ctrl.SetDate(wx.DateTimeFromDMY(*new_date))
            evt.Skip()

        calendar_ctrl.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED, OnCalendar)

        panel.sizer.Add(device_ctrl)
        panel.sizer.Add(calendar_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        panel.sizer.Add(display_ctrl)

        while panel.Affirmed():
            date = calendar_ctrl.GetDate()
            panel.SetResult(
                device_ctrl.GetStringSelection(),
                date.GetDay(),
                date.GetMonth() + 1,
                date.GetYear(),
                display_ctrl.GetValue()
            )

    def _check_device(self, d):
        return d.has_emeter


class ChangeAlias(eg.ActionBase):
    name = 'Change Device Alias'
    description = 'Change the alias (user given name) of a device.'

    def GetLabel(self, device, alias):
        return '%s: %s %s' % (self.name, device, alias)

    def __call__(self, device, alias):

        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, dvc.id):
                dvc.alias = alias
                return True

        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return False

    def _check_device(self, _):
        return True

    def Configure(self, device='', alias=''):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            device,
            self._check_device
        )

        alias_st = panel.StaticText('Alias:')
        alias_ctrl = panel.TextCtrl(alias)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(alias_st, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(alias_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(device_ctrl)
        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.GetStringSelection(),
                alias_ctrl.GetValue()
            )


class ChangeEMeterGains(eg.ActionBase):
    name = 'Change Device EMeter Gains'
    description = 'Change the emeter gains in a device.'

    def _check_device(self, device):
        return device.has_emeter

    def Configure(self):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            '',
            self._check_device
        )

        vgain_st = panel.StaticText('V Gain:')
        vgain_ctrl = panel.SpinIntCtrl(0)

        igain_st = panel.StaticText('I Gain:')
        igain_ctrl = panel.SpinIntCtrl(0)

        panel.dialog.buttonRow.okButton.Hide()
        panel.dialog.buttonRow.testButton.Hide()
        panel.dialog.buttonRow.cancelButton.Hide()

        set_btn = panel.dialog.buttonRow.applyButton
        set_btn.Unbind(wx.EVT_BUTTON)

        set_btn.SetLabel('Set Gains')
        set_btn.Enable(False)

        def on_set(evt):
            device = device_ctrl.GetStringSelection()
            set_btn.Enable(False)
            for dvc in tp_link:
                if device in (dvc.alias, dvc.ip, dvc.id):
                    dvc.emeter.gain = (
                        vgain_ctrl.GetValue(),
                        igain_ctrl.GetValue()
                    )
                    break

        def on_device(evt):
            device = device_ctrl.GetStringSelection()

            for dvc in tp_link:
                if device in (dvc.alias, dvc.ip, dvc.id):
                    set_btn.Enable(True)
                    gains = dvc.emeter.gain
                    vgain_ctrl.SetValue(gains['vgain'])
                    igain_ctrl.SetValue(gains['igain'])
                    break

        device_ctrl.Bind(wx.EVT_CHOICE, on_device)
        set_btn.Bind(wx.EVT_BUTTON, on_set)

        vgain_sizer = wx.BoxSizer(wx.HORIZONTAL)
        vgain_sizer.Add(vgain_st, 0, wx.EXPAND | wx.ALL, 5)
        vgain_sizer.Add(vgain_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        igain_sizer = wx.BoxSizer(wx.HORIZONTAL)
        igain_sizer.Add(igain_st, 0, wx.EXPAND | wx.ALL, 5)
        igain_sizer.Add(igain_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(device_ctrl)
        panel.sizer.Add(vgain_sizer)
        panel.sizer.Add(igain_sizer)

        while panel.Affirmed():
            panel.SetResult()


class EMeterCalibration(eg.ActionBase):
    name = 'Calibrate EMeter'
    description = 'Calibrate the emeter on a device.'

    def _check_device(self, device):
        return device.has_emeter

    def Configure(self):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            '',
            self._check_device
        )

        vtarget_st = panel.StaticText('V Target:')
        vtarget_ctrl = panel.SpinIntCtrl(0)

        itarget_st = panel.StaticText('I Target:')
        itarget_ctrl = panel.SpinIntCtrl(0)

        panel.dialog.buttonRow.okButton.Hide()
        panel.dialog.buttonRow.testButton.Hide()
        panel.dialog.buttonRow.cancelButton.Hide()

        start_btn = panel.dialog.buttonRow.applyButton
        start_btn.Unbind(wx.EVT_BUTTON)

        start_btn.SetLabel('Start Calibration')
        start_btn.Enable(False)

        def on_start(evt):
            device = device_ctrl.GetStringSelection()

            start_btn.Enable(False)
            for dvc in tp_link:
                if device in (dvc.alias, dvc.ip, dvc.id):
                    dvc.emeter.calibration = (
                        vtarget_ctrl.GetValue(),
                        itarget_ctrl.GetValue()
                    )
                    break

        def on_device(evt):
            start_btn.Enable(True)

        device_ctrl.Bind(wx.EVT_CHOICE, on_device)
        start_btn.Bind(wx.EVT_BUTTON, on_start)

        vtarget_sizer = wx.BoxSizer(wx.HORIZONTAL)
        vtarget_sizer.Add(vtarget_st, 0, wx.EXPAND | wx.ALL, 5)
        vtarget_sizer.Add(vtarget_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        itarget_sizer = wx.BoxSizer(wx.HORIZONTAL)
        itarget_sizer.Add(itarget_st, 0, wx.EXPAND | wx.ALL, 5)
        itarget_sizer.Add(itarget_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(device_ctrl)
        panel.sizer.Add(vtarget_sizer)
        panel.sizer.Add(itarget_sizer)

        while panel.Affirmed():
            panel.SetResult()


class CloudServer(eg.ActionBase):
    name = 'Cloud Server Bindings'
    description = 'Binds and unbinds to the cloud server.'

    def _check_device(self, _):
        return True

    def Configure(self):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            '',
            self._check_device
        )

        panel.dialog.buttonRow.okButton.Hide()
        panel.dialog.buttonRow.testButton.Hide()

        bind_btn = panel.dialog.buttonRow.applyButton
        unbind_btn = panel.dialog.buttonRow.cancelButton

        bind_btn.Unbind(wx.EVT_BUTTON)
        unbind_btn.Unbind(wx.EVT_BUTTON)

        bind_btn.SetLabel('Bind')
        unbind_btn.SetLabel('Unbind')

        bind_btn.Enable(False)
        unbind_btn.Enable(False)

        def on_device(evt):
            bind_btn.Unbind(wx.EVT_BUTTON)
            bind_btn.Enable(False)

            unbind_btn.Unbind(wx.EVT_BUTTON)
            unbind_btn.Enable(False)

            device = device_ctrl.GetStringSelection()

            for dvc in tp_link:
                if device in (dvc.alias, dvc.ip, dvc.id):
                    cloud_status = dvc.cloud_server
                    print(cloud_status)

                    def on_unbind(evt):
                        dvc.cloud_server_unbind()
                        unbind_btn.Unbind(wx.EVT_BUTTON)
                        unbind_btn.Enable(False)
                        bind_btn.Bind(wx.EVT_BUTTON, on_bind)
                        bind_btn.Enable(True)

                    def on_bind(evt):
                        username = str(input('Cloud Server Username'))
                        password = str(input('Cloud Server Password'))
                        dvc.cloud_server_bind(username, password)
                        bind_btn.Unbind(wx.EVT_BUTTON)
                        bind_btn.Enable(False)
                        unbind_btn.Bind(wx.EVT_BUTTON, on_unbind)
                        unbind_btn.Enable(True)

                    if cloud_status:
                        unbind_btn.Bind(wx.EVT_BUTTON, on_unbind)
                        unbind_btn.Enable(True)
                    else:
                        bind_btn.Bind(wx.EVT_BUTTON, on_bind)
                        bind_btn.Enable(True)

        device_ctrl.Bind(wx.EVT_CHOICE, on_device)
        panel.sizer.Add(device_ctrl)

        while panel.Affirmed():
            panel.SetResult()


class FlashFirmware(eg.ActionBase):
    name = 'Flash Firmware'
    description = 'Flashes firmware.'

    def _check_device(self, _):
        return True

    def Configure(self):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            '',
            self._check_device
        )

        fw_st = panel.StaticText('Firmware:')
        fw_ctrl = panel.Choice(0, choices=[''])

        panel.dialog.buttonRow.okButton.Hide()
        panel.dialog.buttonRow.testButton.Hide()

        flash_btn = panel.dialog.buttonRow.applyButton
        download_btn = panel.dialog.buttonRow.cancelButton

        download_btn.Unbind(wx.EVT_BUTTON)
        flash_btn.Unbind(wx.EVT_BUTTON)

        download_btn.SetLabel('Not Ready')
        flash_btn.SetLabel('Not Ready')

        download_btn.Enable(False)
        flash_btn.Enable(False)
        fw_ctrl.Enable(False)

        timer = None
        cloud_unbind = None

        def on_device(evt):
            global timer
            global cloud_unbind

            if cloud_unbind is not None:
                cloud_unbind()
                cloud_unbind = None

            fw_ctrl.SetItems([''])
            download_btn.Unbind(wx.EVT_BUTTON)
            download_btn.SetLabel('Not Ready')
            download_btn.Enable(False)

            flash_btn.Unbind(wx.EVT_BUTTON)
            flash_btn.SetLabel('Not Ready')
            flash_btn.Enable(False)

            if timer is not None:
                timer.Stop()
                timer = None

            device = device_ctrl.GetStringSelection()

            for dvc in tp_link:
                if device in (dvc.alias, dvc.ip, dvc.id):
                    cloud_status = dvc.cloud_server
                    print(cloud_status)
                    if not cloud_status:
                        username = str(input('Cloud Server Username'))
                        password = str(input('Cloud Server Password'))
                        dvc.cloud_server_bind(username, password)
                        cloud_unbind = dvc.cloud_server_unbind

                    fw_list = dvc.firmware.firmware_list
                    print(fw_list)
                    fw_ctrl.SetItems(fw_list)
                    fw_ctrl.Enable(True)

        def on_fw(evt):
            flash_btn.Unbind(wx.EVT_BUTTON)
            download_btn.Unbind(wx.EVT_BUTTON)
            flash_btn.SetLabel('Not Ready')
            flash_btn.Enable(False)

            fw = fw_ctrl.GetStringSelection()
            if fw:
                device = device_ctrl.GetStringSelection()

                for dvc in tp_link:
                    if device in (dvc.alias, dvc.ip, dvc.id):
                        download_btn.SetLabel('Download!')
                        download_btn.Enable(True)

                        def on_download(evt):
                            global timer

                            download_btn.Unbind(wx.EVT_BUTTON)
                            download_btn.SetLabel('Not Ready')
                            download_btn.Enable(False)
                            dvc.firmware_download_url(fw)

                            def on_timer(evt):
                                global timer

                                dl_state = dvc.firmware.download_state
                                print(dl_state)

                                if dl_state == '100':
                                    flash_btn.Enable(True)
                                    flash_btn.SetLabel('Flash!')
                                    timer = None

                                    def on_flash(evt):
                                        flash_btn.Unbind(wx.EVT_BUTTON)
                                        flash_btn.SetLabel('Not Ready')
                                        flash_btn.Enable(False)
                                        dvc.firmware.download_flash()

                                    flash_btn.Bind(wx.EVT_BUTTON, on_flash)

                                else:
                                    flash_btn.SetLabel(dl_state)
                                    timer.Restart()

                            timer = wx.CallLater(500, on_timer)
                            timer.Start()

                        download_btn.Bind(wx.EVT_BUTTON, on_download)
                        return

            download_btn.SetLabel('Not Ready')
            download_btn.Enable(False)

        device_ctrl.Bind(wx.EVT_CHOICE, on_device)
        fw_ctrl.Bind(wx.EVT_CHOICE, on_fw)

        fw_sizer = wx.BoxSizer(wx.HORIZONTAL)
        fw_sizer.Add(fw_st, 0, wx.EXPAND | wx.ALL, 5)
        fw_sizer.Add(fw_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(device_ctrl)
        panel.sizer.Add(fw_sizer)

        while panel.Affirmed():
            panel.SetResult()

        if timer is not None:
            timer.Stop()

        if cloud_unbind is not None:
            cloud_unbind()


class RebootDevice(eg.ActionBase):
    name = 'Reboot Device'
    description = 'Reboot a device.'

    def GetLabel(self, device, delay):
        return '%s: %s %s' % (self.name, device, delay)

    def __call__(self, device, delay):

        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, dvc.id):
                dvc.system.reboot(delay)
                return True

        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return False

    def _check_device(self, _):
        return True

    def Configure(self, device='', delay=1):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            device,
            self._check_device
        )

        delay_st = panel.StaticText('Delay (seconds):')
        delay_ctrl = panel.SpinIntCtrl(delay, min=1)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(delay_st, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(delay_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(device_ctrl)
        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.GetStringSelection(),
                delay_ctrl.GetValue()
            )


class TestUBoot(eg.ActionBase):
    name = 'Test uBoot'
    description = 'Perform uBoot boot loader check.'

    def GetLabel(self, device):
        return '%s: %s' % (self.name, device)

    def __call__(self, device):

        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, dvc.id):
                dvc.service.test_uboot()
                return True

        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return False

    def _check_device(self, _):
        return True

    def Configure(self, device=''):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            device,
            self._check_device
        )

        panel.sizer.Add(device_ctrl)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.GetStringSelection(),
            )


class ResetDevice(eg.ActionBase):
    name = 'Reset Device'
    description = 'Reset a device to factory defaults.'

    def GetLabel(self, device, delay):
        return '%s: %s %s' % (self.name, device, delay)

    def __call__(self, device, delay):

        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, dvc.id):
                dvc.system.reset(delay)
                return True

        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return False

    def _check_device(self, _):
        return True

    def Configure(self, device='', delay=1):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            device,
            self._check_device
        )

        delay_st = panel.StaticText('Delay (seconds):')
        delay_ctrl = panel.SpinIntCtrl(delay, min=1)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(delay_st, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(delay_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(device_ctrl)
        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.GetStringSelection(),
                delay_ctrl.GetValue()
            )


class ClearEMeter(eg.ActionBase):
    name = 'Clear Meter Readings'
    description = 'Clear a devices meter readings (if supported).'

    def __call__(self, device):

        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, dvc.id):
                if self._check_device(dvc):
                    res = dvc.emeter.erase_emeter_stats()
                    return res
                else:
                    eg.PrintNotice(
                        '%s: Device %s does not have an EMeter.' %
                        (self.name, device)
                    )
                    return
        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return False

    def _check_device(self, device):
        return device.has_emeter

    def Configure(self, device=''):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(
            panel,
            device,
            self._check_device
        )

        panel.sizer.Add(device_ctrl)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.GetStringSelection(),
            )


class GetDevice(eg.ActionBase):
    name = 'Get Device'

    def __call__(self, device):
        for dvc in tp_link:
            if device in (dvc.alias, dvc.ip, dvc.id):
                return dvc

        eg.PrintNotice(
            '%s: Device %s not found.' %
            (self.name, device)
        )
        return None


class Schedule(eg.ActionBase):
    def Configure(self):
        panel = eg.ConfigPanel()

        import fold_panel

        ctrl = fold_panel.DeviceFoldPanel(panel)

        panel.sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)

        while panel.Affirmed():
            panel.SetResult()


class AllOn(eg.ActionBase):
    pass


class AllOff(eg.ActionBase):
    pass


class AllAntiTheft(eg.ActionBase):
    pass





'''
SCHEDULE
        "eact": int(-1) end action 0 = OFF, 1 = ON
        "sact": int(1), start action 0 = OFF, 1 = ON


        "wday":list(0, 1, 0, 1, 1, 0, 0), 0 or a 1 for each day of the week
                                          1 representing a scheduled day

        "enable":int(1), 0 or a 1, 1 being enabled
        "repeat": int(1), 0 or a 1, 1 to repeat

        "day": int(0), 0 for all days of the month
        "month": int(0), 0 for all months
        "year": int(0), 0 for all years

        "etime_opt": int(-1) use end time
        "emin": int(0) end time minute number in the day

        "stime_opt":int(0) use start time
        "smin":int(1014) start time minute number in the day

        "longitude": int/float(0), 0 for all locations
        "latitude": int/float(0), 0 for all locations

        "force": int(0), 0 or 1, 1 to force rule


'''

'''
COUNTDOWN
        "enable": int(1), 0 or a 1, 1 being enabled
        "delay": int(milliseconds)
        "act": int(1)
'''

'''
ALARM
        "duration": int(2)
        "lastfor": int(1)
        "frequency": int(5)
        
        
        "stime_opt":int(0)
        "smin":int(1014)
        
        "etime_opt": int(-1)
        "emin": int(0)
        
        
        "wday":list(0, 1, 0, 1, 1, 0, 0), 0 or a 1 for each day of the week
                                          1 representing a scheduled day
        
        "enable":int(1), 0 or a 1, 1 being enabled
        "repeat": int(1), 0 or a 1, 1 to repeat the schedule
        
        
        "day": int(0), 0 for all days of the month
        "month": int(0), 0 for all months
        "year": int(0), 0 for all years
        
        "longitude": int/float(0), 0 for all locations
        "latitude": int/float(0), 0 for all locations
        
        "force": int(0), 0 or 1, 1 to force schedule
        
        
'''