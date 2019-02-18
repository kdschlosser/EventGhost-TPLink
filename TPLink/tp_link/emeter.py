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


# {
#     "emeter": {
#         "get_realtime": {
#             "current": 0.848669,
#             "err_code": 0,
#             "power": 114.479615,
#             "total": 0.022,
#             "voltage": 240.036493
#         }
#     }
# }

import datetime


class RealTime(object):

    def __init__(self, send, meter_units):
        self._send = send
        self._meter_units = meter_units

    @property
    def current(self):
        res = self._send(get_realtime=dict())
        key = 'current' + self._meter_units
        return res[key]

    @property
    def voltage(self):
        res = self._send(get_realtime=dict())
        key = 'voltage' + self._meter_units
        return res[key]

    @property
    def power(self):
        res = self._send(get_realtime=dict())
        key = 'power' + self._meter_units
        return res[key]

    @property
    def energy(self):
        res = self._send(get_realtime=dict())
        key = 'total' + self._meter_units
        return res[key]

    @property
    def all_readings(self):
        return self._send(get_realtime=dict())


class _EMeter(object):

    def __init__(self, device, meter_units):
        self.device = device
        self._meter_units = meter_units
        self.realtime = RealTime(self._send, meter_units)

    def _send(self, **kwargs):
        return self.device.query(emeter=kwargs)

    def daily(
        self,
        year=datetime.datetime.now().year,
        month=datetime.datetime.now().month
    ):
        """
        Retrieve daily statistics for a given month

        :param year: year for which to retrieve statistics (default: this year)
        :param month: month for which to retrieve statistcs (default: this
                      month)
        :return: mapping of day of month to value
                 False if device has no energy meter or error occured
        :rtype: dict
        :raises SmartPlugException: on error
        """
        res = self._send(get_daystat=dict(month=month, year=year))
        key = 'energy' + self._meter_units
        return dict(
            list(
                (entry['day'], entry[key])
                for entry in res['day_list']
            )
        )

    def monthly(self, year=datetime.datetime.now().year):
        """
        Retrieve monthly statistics for a given year.

        :param year: year for which to retrieve statistics (default: this year)
        :return: dict: mapping of month to value
                 False if device has no energy meter
        :rtype: dict
        :raises SmartPlugException: on error
        """

        res = self._send(get_monthstat=dict(year=year))
        key = 'energy' + self._meter_units
        return dict(
            list(
                (entry['day'], entry[key])
                for entry in res['month_list']
            )
        )

    def erase(self):
        """
        Erase energy meter statistics

        :return: True if statistics were deleted
                 False if device has no energy meter.
        :rtype: bool
        :raises SmartPlugException: on error
        """
        self._send(erase_emeter_stat=None)

    @property
    def current_consumption(self):
        """
        Get the current power consumption in Watt.

        :return: the current power consumption in Watt.
                 False if device has no energy meter.
        :raises SmartPlugException: on error
        """

        return self.realtime.power

    @property
    def gain(self):
        """
        Get EMeter voltage and current gains.

        :return: dict voltage and current gains
        :rtype: dict
        :raises SmartPlugException: on error
        """

        return self._send(
            get_vgain_igain=dict()
        )

    @gain.setter
    def gain(self, (vgain, igain)):
        """
        Set EMeter voltage and current gains.

        :param int vgain: int(voltage_gain)
        :param int igain: int(current_gain)
        :return: None
        :rtype: None
        :raises SmartPlugException: on error
        """
        self._send(
            set_vgain_igain=dict(vgain=vgain, igain=igain)
        )

    @property
    def calibration(self):
        raise NotImplementedError

    @calibration.setter
    def calibration(self, (vtarget, itarget)):
        """
        Starts EMeter calibration.

        :param int vtarget: Voltage target.
        :param int itarget: Current target.
        :return: None
        :rtype: None
        :raises SmartPlugException: on error
        """

        self._send(
            start_calibration=dict(vtarget=vtarget, itarget=itarget)
        )


class EMeter(object):

    def __init__(self, meter_units):
        self.e_meter = _EMeter(self, meter_units)
