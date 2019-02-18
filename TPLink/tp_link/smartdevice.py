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
import netif
import cloud
import dtime
import emeter
import firmware
import hardware
import schedules
import system
import protocol
import TPLinkException
import json
import socket
import struct
from louie import dispatcher
from copy import deepcopy

from tp_link import (
    SIGNAL_STATE_CHANGE,
    SIGNAL_COLOR_CHANGE,
    SIGNAL_KELVIN_CHANGE,
    SIGNAL_TIME_CHANGE,
    SIGNAL_LED_CHANGED,
    SIGNAL_BRIGHTNESS_CHANGE,
    SIGNAL_MODE_CHANGE,
    SIGNAL_ALIAS_CHANGE,
    SIGNAL_LOCATION_CHANGE,
    SIGNAL_DEVICE_ADDED,
    SIGNAL_DEVICE_REMOVED,
    SIGNAL_ANTITHEFT_RULE_CHANGED,
    SIGNAL_ANTITHEFT_RULE_ADDED,
    SIGNAL_ANTITHEFT_RULE_REMOVED,
    SIGNAL_COUNTDOWN_RULE_CHANGED,
    SIGNAL_COUNTDOWN_RULE_ADDED,
    SIGNAL_COUNTDOWN_RULE_REMOVED,
    SIGNAL_SCHEDULE_RULE_CHANGED,
    SIGNAL_SCHEDULE_RULE_ADDED,
    SIGNAL_SCHEDULE_RULE_REMOVED,
    SIGNAL_POWER_CHANGED,
)


class SmartDeviceSingleton(type):
    _instances = {}

    def __instancecheck__(self, instance):
        return isinstance(instance, SmartDeviceBase)

    def __call__(cls, ip, device_data):
        sys_info = device_data['system']['get_sysinfo']
        id = sys_info['deviceId']
        model = sys_info['model'][:5]

        if (ip, id) not in SmartDeviceSingleton._instances.keys():
            if hasattr(smartbulb, model):
                device_cls = getattr(smartbulb, model)
            elif hasattr(smartplug, model):
                device_cls = getattr(smartplug, model)
            elif hasattr(smartswitch, model):
                device_cls = getattr(smartswitch, model)
            else:
                device_cls = SmartDeviceBase

            SmartDeviceSingleton._instances[(ip, id)] = device_cls(
                ip,
                id
            )

        return SmartDeviceSingleton._instances[(ip, id)]


class SmartDeviceBase(object):
    e_meter = None

    def __init__(self, ip, id):
        """
        Create a new SmartDevice instance, identified through its IP address.

        :param str ip: ip address on which the device listens
        :raises SmartPlugException: when unable to communicate with the device
        """
        self.__deactivated = False
        self._ip = ip
        self.__id = id
        self.netif = netif.Netif(self)
        self.cloud = cloud.Cloud(self)
        self.time = dtime.DTime(self)
        self.anti_theft = schedules.AntiTheft(self)
        self.count_down = schedules.Countdown(self)
        self.schedule = schedules.Schedule(self)
        self.system = system.System(self)
        self.firmware = firmware.Firmware(self)
        self.hardware = hardware.Hardware(self)
        self._polling_data = None
        self.__callbacks = []

    def __eq__(self, other):
        try:
            return self.id == other.id
        except AttributeError:
            return False

    @property
    def is_deactivated(self):
        return self.__deactivated

    def polling_data(self, data):
        if data is not None:
            if self.__id != data['system']['get_sysinfo']['deviceId']:
                tp_link.update()

        if (
            self._polling_data is not None and
            self._polling_data != data
        ):

            def trigger_event(e):

                for ignore in ('rssi', 'time', 'on_time'):
                    if ignore in e:
                        return
                for callback in self.__callbacks:
                    callback(e, self)

            def iter_data(new, old, evt=''):
                for new_key, new_value in new.items():
                    if new_key in old:
                        old_value = old[new_key]
                        if old_value != new_value:
                            if (
                                isinstance(new_value, dict) and
                                isinstance(old_value, dict)
                            ):
                                if new_key.startswith('get_'):
                                    iter_data(new_value, old_value, evt)
                                else:
                                    iter_data(
                                        new_value,
                                        old_value,
                                        evt + '.' + new_key
                                    )
                            else:
                                trigger_event(
                                    '{0}.{1}.changed'.format(evt, new_key)[1:]
                                )
                    else:
                        trigger_event(
                            '{0}.{1}.added'.format(evt, new_key)[1:]
                        )
            iter_data(data, self._polling_data)

        self._polling_data = data

    polling_data = property(fset=polling_data)

    def query(self, **kwargs):
        if self.__deactivated:
            return None

        if self._polling_data is not None:
            def get_data(req, resp):
                for key in req.keys():
                    if key.startswith('set_'):
                        return None
                    if key in resp:
                        value = resp[key]
                        if req[key] and isinstance(value, dict):
                            return get_data(req[key], value)
                        return value
                    return resp
            res = get_data(kwargs, self._polling_data)
            if res is not None:
                return res

        data = deepcopy(kwargs)

        if 'system' in data:
            if 'get_sysinfo' not in data['system']:
                data['system']['get_sysinfo'] = dict()
        else:
            data.update(dict(system=dict(get_sysinfo=dict())))

        data = json.dumps(data)
        _LOGGER.debug(">> (%i) %s", len(data), data)

        def send():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            def close_socket():
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                    sock.close()
                except socket.error:
                    pass

            try:
                sock.connect((self._ip, 9999))
            except socket.error:
                close_socket()
                raise TPLinkException.SocketError("Socket Connection Error:")

            sock.send(protocol.encrypt(data))

            buf = bytes()
            length = -1
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                if length == -1:
                    length = struct.unpack(">I", chunk[0:4])[0]
                buf += chunk
                if length > 0 and len(buf) >= length + 4:
                    break

            close_socket()

            if not len(buf):
                raise TPLinkException.CorruptedDataError('No Data Received')

            return protocol.decrypt(buf[4:])

        try:
            response = send()
        except TPLinkException.SocketError:
            tp_link.update()
            response = send()

        response = json.loads(response)

        if self.__id != response['system']['get_sysinfo']['deviceId']:
            tp_link.update()
            response = send()
            response = json.loads(response)

        log_data = json.dumps(response)
        _LOGGER.debug("<< (%i) %s", len(log_data), log_data)

        if 'system' not in kwargs:
            del response['system']
        elif 'system' in kwargs and 'get_sysinfo' not in kwargs['system']:
            del response['system']['get_sysinfo']

        target = kwargs.keys()[0]
        if target not in response:
            raise TPLinkException.DeviceError(
                "No required {0} in response: {1}".format(target, response)
            )

        result = response[target]

        if len(kwargs.keys()) == 1 and kwargs.keys()[0] in result:
            result = result[kwargs.keys()[0]]

        if "err_code" in result:
            if result["err_code"] != 0:
                raise TPLinkException.NotSupportedError(
                    "Error on {}.{}: {}".format(target, kwargs, result)
                )
            del result["err_code"]

        return result

    def copy_device(self, new_device):
        self = new_device

    def deactivate(self):
        self.__deactivated = True

    @property
    def ip(self):
        return self._ip

    @property
    def has_emeter(self):
        return isinstance(self, emeter.EMeter)

    @property
    def features(self):
        """
        Returns features of the devices

        :return: list of features
        :rtype: list
        """
        features = self.system.feature.split(':')
        return features

    @property
    def model(self):
        """
        Get model of the device

        :return: device model
        :rtype: str
        :raises SmartPlugException: on error
        """
        return self.system.model

    @property
    def active_mode(self):
        return self.system.active_mode

    @property
    def alias(self):
        """
        Get current device alias (name)

        :return: Device name aka alias.
        :rtype: str
        """
        return self.system.alias

    @alias.setter
    def alias(self, alias):
        """
        Sets the device name aka alias.

        :param alias: New alias (name)
        :raises SmartPlugException: on error
        """
        self.system.alias = alias

    @property
    def icon(self):
        """
        Returns device icon

        Note: not working on HS110, but is always empty.

        :return: icon and its hash
        :rtype: dict
        :raises SmartPlugException: on error
        """
        return self.system.icon_hash

    @icon.setter
    def icon(self, icon):
        """
        Content for hash and icon are unknown.

        :param str icon: Icon path(?)
        :raises NotImplementedError: when not implemented
        :raises SmartPlugError: on error
        """
        raise NotImplementedError(
            "Values for this call are unknown at this point."
        )
        # here just for the sake of completeness
        # self.system.dev_icon = dict(icon="", hash="")

    @property
    def latitude_longitude(self):
        """
        Location of the device, as read from sysinfo

        :return: latitude and longitude
        :rtype: dict
        """
        return self.system.latitude, self.system.longitude

    @latitude_longitude.setter
    def latitude_longitude(self, (latitude, longitude)):
        """
        Sets new location

        :param (latitude, longitude): latitude and longitude
        :raises SmartPlugException: on error
        """

        self.system.dev_location = dict(latitude=latitude, longitude=longitude)

    @property
    def geo_location(self):
        """
        Sets the latitude and longitude using a physical street address.

        To use this feature you need to set the Google API key.

        >>> import tp_link
        >>> tp_link.geocoding.APIKEY = 'YOUR API KEY'

        Getter:
            Returns a formatted string of the physical address
        Setter:
            param (address, city, state):
                There is a single parameter you need to pass a tuple
                containing (street address, city, state/province/country).
        """
        geocoding = __import__(__name__.rsplit('.', 1)[0]).geocoding

        if geocoding.API_KEY:
            return geocoding.get_location(*self.latitude_longitude)
        else:
            raise RuntimeError('Google geocoding API key has not been set.')

    @geo_location.setter
    def geo_location(self, (address, city, state)):
        geocoding = __import__(__name__.rsplit('.', 1)[0]).geocoding

        if geocoding.API_KEY:
            latitude, longitude = geocoding.get_latlon(address, city, state)
            self.latitude_longitude = (latitude, longitude)
        else:
            raise RuntimeError('Google geocoding API key has not been set.')

    @property
    def rssi(self):
        """
        Returns WiFi signal strength (rssi)

        :return: rssi
        :rtype: int
        """
        return self.system.rssi

    @property
    def type(self):
        return self.system.type

    def reboot(self, delay=1):
        """
        Reboot device.

        :param delay: delay in seconds until reboot
        :return: None
        """
        self.system.reboot(delay=delay)

    def reset(self, delay=1):
        """
        Reset device to factory defaults.

        :param delay: delay in seconds until reboot
        :return: None
        :rtype: None
        :raises SmartPlugException: on error
        """
        self.system.reset(delay=delay)

    @property
    def id(self):
        """
        Gets the device id.

        :return: Device id
        :rtype: str
        :raises SmartPlugException: on error
        """
        return self.__id

    @property
    def oem_id(self):
        try:
            return self.system.oemId
        except AttributeError:
            return 'N/A'

    @property
    def mac(self):
        """
        Returns mac address

        :return: mac address in hexadecimal with colons, e.g. 01:23:45:67:89:ab
        :rtype: str
        """

        mac = self.system.mac

        if ':' not in mac:
            mac = ':'.join(a + b for a, b in zip(mac, mac))
        return mac.upper()

    @property
    def dev_name(self):
        try:
            return self.system.dev_name
        except AttributeError:
            return 'N/A'


class SmartDevice(SmartDeviceBase):

    __metaclass__ = SmartDeviceSingleton

    def __init__(self, ip, id):
        self.ip = ip
        self.id = id


import smartbulb
import smartplug
import smartswitch
tp_link = __import__(__name__.rsplit('.', 1)[0])


