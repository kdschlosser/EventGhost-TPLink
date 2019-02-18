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

import datetime


class DTime(object):
    """
    "time": {
            "get_time": {
                "mday": 28,
                "hour": 0,
                "min": 23,
                "month": 6,
                "sec": 11,
                "year": 2018,
                "wday": 4,
                "err_code": 0
            },
            "get_timezone": {
                "index": 10,
                "dst_offset": 60,
                "tz_str": "MST7MDT,M3.2.0,M11.1.0",
                "zone_str": "(UTC-07:00) Mountain Daylight Time (US & Canada)",
                "err_code": 0
            }
    """

    def __init__(self, device):
        self.device = device

    def _send(self, **kwargs):
        res = self.device.query(time=kwargs)

        if 'time' in res:
            res = res['time']

        if len(res.keys()) == 1:
            res = res[res.keys()[0]]

        return res

    def __str__(self):
        return '{hour}:{min}:{sec} {mday}/{month}/{year}'.format(
            **self._send(get_time=dict())
        )

    def __unicode__(self):
        return unicode(str(self))

    def set(self, ts=datetime.datetime.now()):
        """
        :param datetime.datetime ts: New date and time
        :return: None
        :rtype: None
        :raises SmartPlugException: on error
        """

        utc_offset = self.timezone['index']

        ts = dict(
            hour=ts.hour,
            min=ts.minute,
            sec=ts.second,
            year=ts.year,
            month=ts.month,
            mday=ts.day,
            index=utc_offset
        )
        self._send(set_timezone=ts)

    @property
    def year(self):
        return self._send(get_time=dict())['year']

    @year.setter
    def year(self, year):
        data = self._send(get_time=dict())
        data['year'] = year
        self._send(set_timezone=data)

    @property
    def day(self):
        return self._send(get_time=dict())['mday']

    @day.setter
    def day(self, day):
        data = self._send(get_time=dict())
        data['mday'] = day
        self._send(set_timezone=data)

    @property
    def month(self):
        return self._send(get_time=dict())['month']

    @month.setter
    def month(self, month):
        data = self._send(get_time=dict())
        data['month'] = month
        self._send(set_timezone=data)

    @property
    def minute(self):
        return self._send(get_time=dict())['min']

    @minute.setter
    def minute(self, minute):
        data = self._send(get_time=dict())
        data['min'] = minute
        self._send(set_timezone=data)

    @property
    def hour(self):
        return self._send(get_time=dict())['hour']

    @hour.setter
    def hour(self, hour):
        data = self._send(get_time=dict())
        data['hour'] = hour
        self._send(set_timezone=data)

    @property
    def second(self):
        return self._send(get_time=dict())['sec']

    @second.setter
    def second(self, second):
        data = self._send(get_time=dict())
        data['sec'] = second
        self._send(set_timezone=data)

    @property
    def timezone(self):
        """
        Returns timezone information

        :return: Timezone information
        :rtype: dict
        :raises SmartPlugException: on error
        """
        res = self._send(get_timezone=dict())
        print res
        return res

    @timezone.setter
    def timezone(self, timezone):
        data = self._send(get_time=dict())
        data['index'] = timezone
        self._send(set_timezone=data)
