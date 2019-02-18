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

import rule


class GetRules(object):
    _key = None

    def __init__(self, device):
        self.device = device
        self._rules = []

    def _send(self, **kwargs):
        kwargs = {self._key: kwargs}
        return self.device.query(**kwargs)

    @property
    def _get_rules(self):
        # {'schedule': {
        #   'get_daystat': {'month': month, 'year': year}
        # }}
        # {'schedule': {'get_rules': {}}}

        """
        Gets all rules.

        :return: list rules
        :rtype: list
        :raises SmartPlugException: on error
        """
        return self._send(get_rules=None)['rule_list']

    def update(self):
        rules = []

        for r1 in self._get_rules:
            for r2 in self._rules:
                if r1['id'] == r2.id:
                    r2.update()
                    rules += [r2]
                    self._rules.remove(r2)
                    break
            else:
                if isinstance(self, Schedule):
                    func = rule.ScheduleRule
                elif isinstance(self, AntiTheft):
                    func = rule.AntiTheftRule
                else:
                    func = rule.CountdownRule

                rules += [func(self.device, **r1)]

        del self._rules[:]
        self._rules = rules[:]

    def __iter__(self):
        """
        Iterates all rules.

        :return: iterator (name, rule)
        :rtype: iterator
        :raises SmartPlugException: on error
        """
        self.update()

        for r in self._rules:
            yield r

    def __contains__(self, name):
        """
        Checks if rule name exists.

        :param str name: Name of the rule.
        :return: bool True if name exists else False
        :rtype: bool
        :raises SmartPlugException: on error
        """
        for r in self:
            if r.name == name:
                return True
        return False

    def __delitem__(self, name):
        """
        Deletes rule.

        :param str name: Name of the rule.
        :return: None
        :rtype: None
        :raises Schedule.NoScheduleFound: If rule not found
        :raises SmartPlugException: on error
        """
        for r in self:
            if r.name == name:
                self._rules.remove(r)
                if r.id is not None:
                    self._send(delete_rule=dict(id=r.id))
                break
        else:
            raise self.__class__.NoRuleFound(name)

    def next(self):
        """
        Gets next rule

        :return: dict rule: Next rule to run
        :rtype: dict
        :raises Schedule.NoScheduleFound: If rule not found
        :raises SmartPlugException: on error
        """
        r1 = self._send(get_next_action=None)
        for r2 in self._rules:
            if r1['id'] == r2.id:
                return r2

    def new(self):
        if isinstance(self, Schedule):
            func = rule.ScheduleRule
        elif isinstance(self, AntiTheft):
            func = rule.AntiTheftRule
        else:
            func = rule.CountdownRule

        return func(self._device, self._ip)

    def __getitem__(self, name):
        """
        Gets rule

        :param str name: Name of the rule.
        :return: dict rule
        :rtype: dict
        :raises Schedule.NoScheduleFound: If rule not found
        :raises SmartPlugException: on error
        """
        for r in self:
            if r.name == name:
                return r

        raise self.__class__.NoRuleFound(name)

    def delete_all_rules(self):
        """
        Deletes all rules.

        :return: None
        :rtype: None
        :raises SmartPlugException: on error
        """
        self._send(delete_all_rules=None)
        self._send(erase_runtime_stat=None)

    class NoRuleFound(Exception):

        def __init__(self, name):
            self.msg = 'There is no rule by the name %s.' % name

        def __str__(self):
            return self.msg


class Schedule(GetRules):
    """
    "schedule": {
            "get_rules": {
                "rule_list": [
                    {
                        "etime_opt": -1,
                        "enable": 1,
                        "name": "",
                        "emin": 0,
                        "eact": -1,
                        "month": 0,
                        "sact": 1,
                        "repeat": 1,
                        "smin": 24,
                        "year": 0,
                        "wday": [
                            0,
                            1,
                            0,
                            0,
                            0,
                            0,
                            0
                        ],
                        "id": "6EAC0129E3FB860F9E94E3F9C6EA8E46",
                        "day": 0,
                        "stime_opt": 0
                    }
                ],
                "enable": 1,
                "err_code": 0
            }
        },
    """
    _key = "schedule"


class Countdown(GetRules):
    """
    "count_down": {
            "get_rules": {
                "rule_list": [
                    {
                        "enable": 1,
                        "name": "add timer",
                        "delay": 1800,
                        "remain": 1796,
                        "act": 1,
                        "id": "19F27821AD48EC9CF0FDE926211176B3"
                    }
                ],
                "err_code": 0
            }
        },
    """
    _key = "count_down"


class AntiTheft(GetRules):
    """
    "anti_theft": {
            "get_rules": {
                "rule_list": [
                    {
                        "etime_opt": 0,
                        "enable": 1,
                        "name": "",
                        "emin": 504,
                        "day": 0,
                        "month": 0,
                        "frequency": 5,
                        "smin": 457,
                        "year": 0,
                        "wday": [
                            1,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0
                        ],
                        "id": "D2E7502EAA0CFB64A38318887F208CE9",
                        "repeat": 1,
                        "stime_opt": 0
                    }
                ],
                "enable": 1,
                "err_code": 0
            }
        }
    """
    _key = "anti_theft"
