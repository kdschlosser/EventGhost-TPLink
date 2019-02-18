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

import requests
import json
import urllib

API_KEY = 'AIzaSyBsB-00AjLqCtBzOPWBhSYEjdf7Gb9itoE'
LOCATION_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'
LATLON_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'


def get_location(lat, lon):
    url = dict(
        key=API_KEY,
        latlng=str(lat) + ',' + str(lon)
    )
    url = LOCATION_URL + urllib.urlencode(url)
    try:
        response = requests.get(url)
        return json.loads(response.content)['results'][0]['formatted_address']

    except (requests.HTTPError, ValueError, KeyError, IndexError):
        return None


def get_latlon(address, city, state):
    url = dict(
        key=API_KEY,
        address='{0}, {1}, {2}'.format(address, city, state)
    )
    url = LATLON_URL + urllib.urlencode(url)
    try:
        response = requests.get(url)
        latlon = json.loads(
            response.content
        )['results'][0]['geometry']['location']

        return latlon['lat'], latlon['lng']

    except (requests.HTTPError, ValueError, KeyError, IndexError):
        return None
