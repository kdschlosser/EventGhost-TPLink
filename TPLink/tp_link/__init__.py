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

import geocoding
from TPLinkException import *


class _DeviceContainer(object):
    def __init__(self):
        import threading

        self.__lock = threading.RLock()
        self.__devices = []

    def __getitem__(self, item):
        with self.__lock:
            if isinstance(item, (int, slice)):
                return self.__devices[item]

            for device in self.__devices:
                if item in (device.ip, device.alias, device.id):
                    return device

            raise KeyError(item)

    def __contains__(self, item):
        with self.__lock:
            try:
                self.__getitem__(item)
                return True
            except KeyError:
                return False

    def __getslice__(self, i, j):
        with self.__lock:
            return self.__devices[i:j]

    def __iadd__(self, other):
        with self.__lock:
            self.__devices += other
            return self

    def __len__(self):
        with self.__lock:
            return len(self.__devices)

    def __iter__(self):
        with self.__lock:
            for device in self.__devices:
                yield device

    def remove(self, instance):
        with self.__lock:
            self.__devices.remove(instance)


class TPLink(object):
    SIGNAL_STATE_CHANGE = 'State.Changed'
    SIGNAL_COLOR_CHANGE = 'Color.Changed'
    SIGNAL_KELVIN_CHANGE = 'ColorTemp.Changed'
    SIGNAL_TIME_CHANGE = 'Time.Changed'
    SIGNAL_LED_CHANGED = 'LED.Changed'
    SIGNAL_BRIGHTNESS_CHANGE = 'Brightness.Changed'
    SIGNAL_MODE_CHANGE = 'Mode.Changed'
    SIGNAL_ALIAS_CHANGE = 'Alias.Changed'
    SIGNAL_LOCATION_CHANGE = 'Location.Changed'
    SIGNAL_DEVICE_ADDED = 'Device.Added'
    SIGNAL_DEVICE_REMOVED = 'Device.Removed'
    SIGNAL_ANTITHEFT_RULE_CHANGED = 'AntiTheft.Rule.Changed'
    SIGNAL_ANTITHEFT_RULE_ADDED = 'AntiTheft.Rule.Added'
    SIGNAL_ANTITHEFT_RULE_REMOVED = 'AntiTheft.Rule.Removed'
    SIGNAL_COUNTDOWN_RULE_CHANGED = 'Countdown.Rule.Changed'
    SIGNAL_COUNTDOWN_RULE_ADDED = 'Countdown.Rule.Added'
    SIGNAL_COUNTDOWN_RULE_REMOVED = 'Countdown.Rule.Removed'
    SIGNAL_SCHEDULE_RULE_CHANGED = 'Schedule.Rule.Changed'
    SIGNAL_SCHEDULE_RULE_ADDED = 'Schedule.Rule.Added'
    SIGNAL_SCHEDULE_RULE_REMOVED = 'Schedule.Rule.Removed'
    SIGNAL_POWER_CHANGED = 'Power.Changed'

    __devices = dict(
        bulbs=_DeviceContainer(),
        switches=_DeviceContainer(),
        plugs=_DeviceContainer(),
        other=_DeviceContainer()
    )

    def __init__(self):
        import sys
        import threading

        mod = sys.modules[__name__]
        self.__dict__ = mod.__dict__
        self.__original_mod__ = mod
        sys.modules[__name__] = self

        self.__callbacks = []
        self.__interval = 0.5
        self.__event = threading.Event()
        self.__thread = None
        self.__update_lock = threading.Lock()
        self.__iter_lock = threading.Lock()

    def register_callback(self, callback):
        if callback not in self.__callbacks:
            self.__callbacks += [callback]
        for device in self:
            device.register_callback(callback)

    def unregister_callback(self, callback):
        if callback in self.__callbacks:
            self.__callbacks.remove(callback)
        for device in self:
            device.unregister_callback(callback)

    def start_polling(self, interval=0.5):
        self.__interval = interval

        if self.__thread is None:
            import threading

            t = threading.Thread(target=self.__poll_loop)
            t.daemon = True
            self.__thread = t
            t.start()

    def stop_poll(self):
        if self.__thread is not None:
            self.__event.set()
            self.__thread.join(self.__interval + 1)

    def __poll_loop(self):
        import _discover
        import socket
        import protocol
        import json
        import threading

        events = []

        for lcl_address in _discover.interface_addresses():
            def do(local_address, evt):
                while not self.__event.isSet():
                    devices = []
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.setsockopt(
                            socket.SOL_SOCKET,
                            socket.SO_BROADCAST,
                            1
                        )
                        sock.setsockopt(
                            socket.SOL_SOCKET,
                            socket.SO_REUSEADDR,
                            1
                        )
                        sock.settimeout(self.__interval)
                        sock.bind((local_address, 0))
                        sock.sendto(
                            _discover.DISCOVERY_QUERY[4:],
                            (_discover.QUERY_TARGET, 9999)
                        )

                    except socket.error:
                        continue
                    else:
                        try:
                            while True:
                                data, addr = sock.recvfrom(4096)
                                ip, p = addr
                                info = json.loads(protocol.decrypt(data))

                                for key in (
                                    'schedule',
                                    'count_down',
                                    'anti_theft'
                                ):
                                    try:
                                        err = (
                                            info[key]['get_rules']['err_code']
                                        )
                                        if err == -11:
                                            class Device(object):
                                                @staticmethod
                                                def query(**kwargs):
                                                    return protocol.query(
                                                        ip,
                                                        **kwargs
                                                    )

                                            from dtime import DTime

                                            time_setter = DTime(Device)
                                            time_setter.set()
                                            break
                                    except KeyError:
                                        pass
                                else:
                                    sys_info = info['system']['get_sysinfo']
                                    info['ip'] = ip
                                    info['id'] = sys_info['deviceId']
                                    devices.append(info)
                        except socket.error:
                            if devices:
                                self._update(devices)

                                for new_device in devices:
                                    for old_device in self:
                                        if old_device.id == new_device['id']:
                                            old_device.polling_data = (
                                                new_device
                                            )

                evt.set()

            events += [threading.Event()]
            t = threading.Thread(target=do, args=(lcl_address, events[-1]))
            t.start()

        self.__event.wait()

        for event in events:
            event.wait()

        self.__event.clear()
        self.__thread = None

    def update(self):
        from _discover import discover as _discover
        data = _discover()
        return self._update(data)

    def _update(self, new_devices):
        self.__update_lock.acquire()
        old_devices = list(device for device in self)

        for new_device in new_devices:
            new_device = SmartDevice(new_device['ip'], new_device)
            for callback in self.__callbacks:
                new_device.register_callback(callback)

            def add_new_device():
                if isinstance(new_device, SmartBulb):
                    self.__devices['bulbs'] += [new_device]
                elif isinstance(new_device, SmartSwitch):
                    self.__devices['switches'] += [new_device]
                elif isinstance(new_device, SmartPlug):
                    self.__devices['plugs'] += [new_device]
                else:
                    self.__devices['other'] += [new_device]

            for old_device in old_devices[:]:
                if old_device.id == new_device.id:
                    old_devices.remove(old_device)
                    if isinstance(old_device, SmartBulb):
                        if isinstance(new_device, SmartBulb):
                            old_device.copy_device(new_device)
                        else:
                            self.__devices['bulbs'].remove(old_device)
                            old_device.deactivate()
                            add_new_device()

                    elif isinstance(old_device, SmartPlug):
                        if isinstance(new_device, SmartPlug):
                            old_device.copy_device(new_device)
                        else:
                            self.__devices['plugs'].remove(old_device)
                            old_device.deactivate()
                            add_new_device()

                    elif isinstance(old_device, SmartSwitch):
                        if isinstance(new_device, SmartSwitch):
                            old_device.copy_device(new_device)
                        else:
                            self.__devices['switches'].remove(old_device)
                            old_device.deactivate()
                            add_new_device()
                    else:
                        if (
                            not isinstance(new_device, SmartSwitch) and
                            not isinstance(new_device, SmartPlug) and
                            not isinstance(new_device, SmartBulb)
                        ):
                            old_device.copy_device(new_device)
                        else:
                            self.__devices['other'].remove(old_device)
                            old_device.deactivate()
                            add_new_device()
                    break
            else:
                add_new_device()

        for old_device in old_devices:
            if isinstance(old_device, SmartBulb):
                self.__devices['bulbs'].remove(old_device)
                old_device.deactivate()

            elif isinstance(old_device, SmartPlug):
                self.__devices['plugs'].remove(old_device)
                old_device.deactivate()

            elif isinstance(old_device, SmartSwitch):
                self.__devices['switches'].remove(old_device)
                old_device.deactivate()
            else:
                self.__devices['other'].remove(old_device)
                old_device.deactivate()
        try:
            return new_devices[:]
        finally:
            self.__update_lock.release()

    def discover(self):
        from _discover import discover as _discover

        devices = _discover()

        for device in devices:
            device = SmartDevice(device['ip'], device)

            if isinstance(device, SmartBulb):
                self.__devices['bulbs'] += [device]
            elif isinstance(device, SmartSwitch):
                self.__devices['switches'] += [device]
            elif isinstance(device, SmartPlug):
                self.__devices['plugs'] += [device]
            else:
                self.__devices['other'] += [device]
        return devices

    @property
    def smart_plugs(self):
        return self.__devices['plugs']

    @property
    def smart_bulbs(self):
        return self.__devices['bulbs']

    @property
    def smart_switches(self):
        return self.__devices['switches']

    @property
    def smart_other(self):
        return self.__devices['other']

    def __iter__(self):
        with self.__iter_lock:
            devices = list(device for device in self.__devices['switches'])[:]
            devices += list(device for device in self.__devices['plugs'])[:]
            devices += list(device for device in self.__devices['bulbs'])[:]
            devices += list(device for device in self.__devices['other'])[:]

            for device in devices:
                yield device

    def __contains__(self, item):
        for device in self:
            if item == device:
                return True
        return False

    def __getitem__(self, item):
        for devices in self.__devices.values():
            try:
                return devices[item]
            except KeyError:
                pass

        raise KeyError(item)



SIGNAL_STATE_CHANGE = TPLink.SIGNAL_STATE_CHANGE
SIGNAL_COLOR_CHANGE = TPLink.SIGNAL_COLOR_CHANGE
SIGNAL_KELVIN_CHANGE = TPLink.SIGNAL_KELVIN_CHANGE
SIGNAL_TIME_CHANGE = TPLink.SIGNAL_TIME_CHANGE
SIGNAL_LED_CHANGED = TPLink.SIGNAL_LED_CHANGED
SIGNAL_BRIGHTNESS_CHANGE = TPLink.SIGNAL_BRIGHTNESS_CHANGE
SIGNAL_MODE_CHANGE = TPLink.SIGNAL_MODE_CHANGE
SIGNAL_ALIAS_CHANGE = TPLink.SIGNAL_ALIAS_CHANGE
SIGNAL_LOCATION_CHANGE = TPLink.SIGNAL_LOCATION_CHANGE
SIGNAL_DEVICE_ADDED = TPLink.SIGNAL_DEVICE_ADDED
SIGNAL_DEVICE_REMOVED = TPLink.SIGNAL_DEVICE_REMOVED
SIGNAL_ANTITHEFT_RULE_CHANGED = TPLink.SIGNAL_ANTITHEFT_RULE_CHANGED
SIGNAL_ANTITHEFT_RULE_ADDED = TPLink.SIGNAL_ANTITHEFT_RULE_ADDED
SIGNAL_ANTITHEFT_RULE_REMOVED = TPLink.SIGNAL_ANTITHEFT_RULE_REMOVED
SIGNAL_COUNTDOWN_RULE_CHANGED = TPLink.SIGNAL_COUNTDOWN_RULE_CHANGED
SIGNAL_COUNTDOWN_RULE_ADDED = TPLink.SIGNAL_COUNTDOWN_RULE_ADDED
SIGNAL_COUNTDOWN_RULE_REMOVED = TPLink.SIGNAL_COUNTDOWN_RULE_REMOVED
SIGNAL_SCHEDULE_RULE_CHANGED = TPLink.SIGNAL_SCHEDULE_RULE_CHANGED
SIGNAL_SCHEDULE_RULE_ADDED = TPLink.SIGNAL_SCHEDULE_RULE_ADDED
SIGNAL_SCHEDULE_RULE_REMOVED = TPLink.SIGNAL_SCHEDULE_RULE_REMOVED
SIGNAL_POWER_CHANGED = TPLink.SIGNAL_POWER_CHANGED

TPLink = TPLink()

from smartbulb import SmartBulb
from smartplug import SmartPlug
from smartswitch import SmartSwitch
from smartdevice import SmartDevice

TPLink.SmartBulb = SmartBulb
TPLink.SmartPlug = SmartPlug
TPLink.SmartSwitch = SmartSwitch
TPLink.SmartDevice = SmartDevice

discover = TPLink.discover
smart_plugs = TPLink.smart_plugs
smart_bulbs = TPLink.smart_bulbs
smart_switches = TPLink.smart_switches
smart_other = TPLink.smart_other

if __name__ == '__main__':

    def test_callback(obj, evt):
        print obj
        print evt

    TPLink.discover()
    import time
    TPLink.register_callback(test_callback)
    TPLink.start_polling(0.1)
    time.sleep(0.5)
    d = smart_switches[0]
    d.state = 'ON' if d.state == 'OFF' else 'OFF'
    while True:
        pass

