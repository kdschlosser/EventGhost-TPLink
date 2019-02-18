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


class Rule(object):
    _key = None

    def __init__(
        self,
        device,
        id=None,
        name=None,
        wday=None,
        enable=None,
        repeat=None,
        force=None,
        month=None,
        day=None,
        year=None,
        latitude=None,
        longitude=None,
        smin=None,
        emin=None,
        stime_opt=None,
        etime_opt=None,

    ):
        self._id = id
        self.device = device

        if id is None:
            self._name = ''
            self._wday = [0] * 7
            self._enable = 0
            self._repeat = 0
            self._smin = 0
            self._emin = 0
            self._stime_opt = 0
            self._etime_opt = 0
            self._year = 0
            self._month = 0
            self._day = 0
            self._force = 0
            self._latitude = 0
            self._longitude = 0
        else:
            self._name = name
            self._wday = wday
            self._enable = enable
            self._repeat = repeat
            self._smin = smin
            self._emin = emin
            self._stime_opt = stime_opt
            self._etime_opt = etime_opt
            self._year = year
            self._month = month
            self._day = day
            self._force = force
            self._latitude = latitude
            self._longitude = longitude

    def __dict__(self):
        raise NotImplementedError

    def __iter__(self):
        for key, value in self.__dict__().items():
            yield (key, value)

    def save(self):
        rule = dict()

        def add(attr_name):
            try:
                rule[attr_name] = getattr(self, attr_name)
            except AttributeError:
                pass

        add('name')
        add('wday')
        add('enable')
        add('repeat')
        add('smin')
        add('emin')
        add('stime_opt')
        add('etime_opt')
        add('year')
        add('month')
        add('day')
        add('longitude')
        add('latitude')
        add('force')

        if self._id is None:
            rule = dict(
                add_rule=rule
            )

        else:
            rule['id'] = self._id
            rule = dict(
                edit_rule=rule
            )

        return rule

    def _send(self, **kwargs):
        kwargs = {self._key: kwargs}
        return self.device.query(**kwargs)

    def update(self):
        if self._id is not None:
            rule = self._send(get_rule=dict(id=self._id))["rule_list"][0]
            get = rule.get

            self._name = get('name', None)
            self._wday = get('wday', None)
            self._enable = get('enable', None)
            self._repeat = get('repeat', None)
            self._smin = get('smin', None)
            self._emin = get('emin', None)
            self._stime_opt = get('stime_opt', None)
            self._etime_opt = get('etime_opt', None)
            self._year = get('year', None)
            self._month = get('month', None)
            self._day = get('day', None)
            self._id = get('id', None)
            self._force = get('force', None)
            self._latitude = get('latitude', None)
            self._longitude = get('longitude', None)

            return rule

    @property
    def force(self):
        if self._force is None:
            raise AttributeError
        return bool(self._force)

    @force.setter
    def force(self, value):
        if self._force is None:
            raise AttributeError
        self._force = int(bool(value))

    @property
    def latitude(self):
        if self._latitude is None:
            raise AttributeError
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if self._latitude is None:
            raise AttributeError
        self._latitude = value

    @property
    def longitude(self):
        if self._longitude is None:
            raise AttributeError
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if self._longitude is None:
            raise AttributeError
        self._longitude = value

    @property
    def id(self):
        if self._force is None:
            raise AttributeError
        return self._id

    @property
    def name(self):
        if self._name is None:
            raise AttributeError
        return self._name

    @name.setter
    def name(self, value):
        if self._name is None:
            raise AttributeError
        self._name = value

    @property
    def wday(self):
        if self._wday is None:
            raise AttributeError

        return self._wday

    @wday.setter
    def wday(self, value):
        if self._wday is None:
            raise AttributeError

        if isinstance(value, tuple) and len(value) == 2:
            index, value = value
            self._wday[index] = value
        else:
            self._wday = value

    @property
    def sunday(self):
        return bool(self._wday[0])

    @sunday.setter
    def sunday(self, flag):
        self.wday = (0, flag)

    @property
    def monday(self):
        return bool(self._wday[1])

    @monday.setter
    def monday(self, flag):
        self.wday = (1, flag)

    @property
    def tuesday(self):
        return bool(self._wday[2])

    @tuesday.setter
    def tuesday(self, flag):
        self.wday = (2, flag)

    @property
    def wednesday(self):
        return bool(self._wday[3])

    @wednesday.setter
    def wednesday(self, flag):
        self.wday = (3, flag)

    @property
    def thursday(self):
        return bool(self._wday[4])

    @thursday.setter
    def thursday(self, flag):
        self.wday = (4, flag)

    @property
    def friday(self):
        return bool(self._wday[5])

    @friday.setter
    def friday(self, flag):
        self.wday = (5, flag)

    @property
    def saturday(self):
        return bool(self._wday[6])

    @saturday.setter
    def saturday(self, flag):
        self.wday = (6, flag)

    @property
    def month(self):
        if self._month is None:
            raise AttributeError
        return self._month

    @month.setter
    def month(self, month):
        if self._month is None:
            raise AttributeError
        self._month = month

    @property
    def year(self):
        if self._year is None:
            raise AttributeError
        return self._year

    @year.setter
    def year(self, year):
        if self._year is None:
            raise AttributeError
        self._year = year

    @property
    def day(self):
        if self._day is None:
            raise AttributeError
        return self._day

    @day.setter
    def day(self, day):
        if self._day is None:
            raise AttributeError
        self._day = day

    @property
    def enabled(self):
        if self._enable is None:
            raise AttributeError
        return bool(self._enable)

    @enabled.setter
    def enabled(self, flag):
        if self._enable is None:
            raise AttributeError
        self._enable = int(bool(flag))

    @property
    def repeat(self):
        if self._repeat is None:
            raise AttributeError
        return bool(self._repeat)

    @repeat.setter
    def repeat(self, flag):
        if self._repeat is None:
            raise AttributeError
        self._repeat = int(bool(flag))

    @property
    def end_time(self):
        if self._emin is None:
            raise AttributeError
        return int((self._emin - (self._emin % 60)) / 60), self._emin % 60

    @end_time.setter
    def end_time(self, (hour, minute)):
        minutes = (hour * 60) + minute

        if self._emin is None:
            raise AttributeError

        self._emin = minutes

        if self._etime_opt is not None:
            self._etime_opt = int(bool(minutes))

    @property
    def start_time(self):
        if self._smin is None:
            raise AttributeError
        return int((self._smin - (self._smin % 60)) / 60), self._smin % 60

    @start_time.setter
    def start_time(self, (hour, minute)):
        minutes = (hour * 60) + minute

        if self._smin is None:
            raise AttributeError

        self._smin = minutes

        if self._stime_opt is not None:
            self._stime_opt = int(bool(minutes))

    def delete(self):
        if self._id is not None:
            self._send(delete_rule=dict(id=self._id))


class ScheduleRule(Rule):
    _key = "schedule"

    def __init__(
        self,
        device,
        id=None,
        sact=0,
        eact=0,
        **kwargs
    ):
        if id is None:
            self._eact = 0
            self._sact = 0
        else:
            self._sact = sact
            self._eact = eact

        Rule.__init__(self, device, id, **kwargs)

    def __dict__(self):
        return dict(
            sact=self._sact,
            eact=self._eact,
            emin=self._emin,
            etime_opt=self._etime_opt,
            smin=self._smin,
            stime_opt=self._stime_opt,
            repeat=self._repeat,
            enable=self._enable,
            day=self._day,
            year=self._year,
            month=self._month,
            wday=self._wday,
            name=self._name,
            id=self._id,
            longitude=self._longitude,
            latitude=self._latitude,
            force=self._force,
        )

    @property
    def end_action(self):
        if self._eact is None:
            raise AttributeError

        return bool(self._eact) if self._eact > -1 else self._eact

    @end_action.setter
    def end_action(self, flag):
        if self._eact is None:
            raise AttributeError

        self._eact = int(bool(flag))

    @property
    def start_action(self):
        if self._sact is None:
            raise AttributeError

        return bool(self._sact) if self._sact > -1 else self._sact

    @start_action.setter
    def start_action(self, flag):
        if self._sact is None:
            raise AttributeError

        self._sact = int(bool(flag))

    def update(self):
        rule = Rule.update(self)

        if rule is not None:
            self._sact = rule.get('sact', None)
            self._eact = rule.get('eact', None)

    def save(self):
        rule = Rule.save(self)
        if self._id is None:
            temp_rule = rule['add_rule']
        else:
            temp_rule = rule['edit_rule']

        if self._sact is not None:
            temp_rule['sact'] = self._sact

        if self._eact is not None:
            temp_rule['eact'] = self._eact

        self._send(**rule)
        self.device.schedule.update()


class AntiTheftRule(Rule):
    _key = "anti_theft"

    def __init__(
        self,
        device,
        id=None,
        frequency=None,
        duration=None,
        lastfor=None,
        **kwargs
    ):
        if id is None:
            self._frequency = 0
            self._duration = 0
            self._lastfor = 0
        else:
            self._frequency = frequency
            self._duration = duration
            self._lastfor = lastfor

        Rule.__init__(self, device, id, **kwargs)

    def __dict__(self):
        return dict(
            frequency=self._frequency,
            duration=self._duration,
            lastfor=self._lastfor,
            emin=self._emin,
            etime_opt=self._etime_opt,
            smin=self._smin,
            stime_opt=self._stime_opt,
            repeat=self._repeat,
            enable=self._enable,
            day=self._day,
            year=self._year,
            month=self._month,
            wday=self._wday,
            name=self._name,
            id=self._id,
            longitude=self._longitude,
            latitude=self._latitude,
            force=self._force,
        )

    @property
    def frequency(self):
        if self._frequency is None:
            raise AttributeError
        return self._frequency

    @frequency.setter
    def frequency(self, minutes):
        if self._frequency is None:
            raise AttributeError
        self._frequency = minutes

    @property
    def duration(self):
        if self._duration is None:
            raise AttributeError
        return self._duration

    @duration.setter
    def duration(self, minutes):
        if self._duration is None:
            raise AttributeError
        self._duration = minutes

    @property
    def lastfor(self):
        if self._lastfor is None:
            raise AttributeError
        return self._lastfor

    @lastfor.setter
    def lastfor(self, minutes):
        if self._lastfor is None:
            raise AttributeError
        self._lastfor = minutes

    def update(self):

        rule = Rule.update(self)

        if rule is not None:
            get = rule.get
            self._lastfor = get('lastfor', None)
            self._duration = get('duration', None)
            self._frequency = get('frequency', None)

    def save(self):
        rule = Rule.save(self)
        if self._id is None:
            temp_rule = rule['add_rule']
        else:
            temp_rule = rule['edit_rule']

        if self._lastfor is not None:
            temp_rule['lastfor'] = self._lastfor
        if self._duration is not None:
            temp_rule['duration'] = self._duration
        if self._frequency is not None:
            temp_rule['frequency'] = self._frequency

        self._send(**rule)
        self.device.anti_theft.update()


class CountdownRule(object):

    def __init__(
        self,
        device,
        id=None,
        enable=None,
        name=None,
        delay=None,
        remain=None,
        act=None
    ):

        self._id = id
        self.device = device

        if id is None:
            self._name = ''
            self._enable = 0
            self._delay = 0
            self._act = 0
            self._remain = 0

        else:
            self._name = name
            self._enable = enable
            self._delay = delay
            self._act = act
            self._remain = remain

    def __dict__(self):
        return dict(
            name=self._name,
            enable=self._enable,
            delay=self._delay,
            act=self._act,
            remain=self._remain
        )

    def __iter__(self):
        for key, value in self.__dict__().items():
            yield (key, value)

    def save(self):
        rule = dict()

        if self._enable is not None:
            rule['enable'] = self._enable
        if self._delay is not None:
            rule['delay'] = self._delay
        if self._act is not None:
            rule['act'] = self._act
        if self._name is not None:
            rule['name'] = self._name

        if self._id is None:
            rule = dict(
                add_rule=rule
            )
        else:
            rule['id'] = self._id
            rule = dict(
                edit_rule=rule
            )

        self._send(**rule)
        self.device.count_down.update()

    def _send(self, **kwargs):
        return self.device.query(count_down=kwargs)

    def update(self):
        if self._id is not None:
            rule = self._send(get_rule=dict(id=self._id))["rule_list"][0]
            get = rule.get
            self._name = get('name', None)
            self._enable = get('enabled', None)
            self._delay = get('delay', None)
            self._act = get('act', None)
            self._remain = get('remain', None)

    @property
    def id(self):
        return self._id

    @property
    def remaining(self):
        if self._remain is None:
            raise AttributeError

        return self._remain

    @property
    def enabled(self):
        if self._enable is None:
            raise AttributeError
        return bool(self._enable)

    @enabled.setter
    def enabled(self, flag):
        if self._enable is None:
            raise AttributeError
        self._enable = int(bool(flag))

    @property
    def delay(self):
        if self._delay is None:
            raise AttributeError
        return self._delay / 1000

    @delay.setter
    def delay(self, seconds):
        if self._delay is None:
            raise AttributeError
        self._delay = seconds * 1000

    @property
    def action(self):
        if self._act is None:
            raise AttributeError
        return bool(self._act)

    @action.setter
    def action(self, flag):
        if self._act is None:
            raise AttributeError
        self._act = int(bool(flag))

    @property
    def name(self):
        if self._name is None:
            raise AttributeError
        return self._name

    @name.setter
    def name(self, value):
        if self._name is None:
            raise AttributeError
        self._name = value

    def delete(self):
        if self._id is not None:
            self._send(delete_rule=dict(id=self._id))
