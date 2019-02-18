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

import json
import socket
import _LOGGER
import protocol
import TPLinkException
import threading

DISCOVERY_QUERY = dict(
    system=dict(get_sysinfo=None),
    emeter=dict(get_realtime=None, get_vgain_igain=None),
    schedule=dict(get_rules=None),
    count_down=dict(get_rules=None),
    anti_theft=dict(get_rules=None),
    time=dict(get_time=None, get_timezone=None),
    cnCloud=dict(get_info=None),
    lightingservice=dict(get_light_details=None)
)

DISCOVERY_QUERY = protocol.encrypt(json.dumps(DISCOVERY_QUERY))
QUERY_TARGET = "255.255.255.255"


def interface_addresses(family=socket.AF_INET):
    for fam, a, b, c, sock_addr in socket.getaddrinfo('', None):
        if family == fam:
            yield sock_addr[0]


def discover(timeout=protocol.DEFAULT_TIMEOUT, port=protocol.DEFAULT_PORT):
    """
    Sends discovery message to 255.255.255.255:9999 in order
    to detect available supported devices in the local network,
    and waits for given timeout for answers from devices.

    :param timeout: How long to wait for responses, defaults to 5
    :param port: port to send broadcast messages, defaults to 9999.
    :rtype: list[dict]
    :return: Array of json objects {"ip", "port", "sys_info"}
    """

    devices = []
    events = []
    global restart
    restart = False

    for lcl_address in interface_addresses():

        def do(local_address, prt, evt):
            dvcs = []
            global restart

            _LOGGER.debug(
                "Sending discovery to 255.255.255.255:%s on local address %s",
                prt,
                local_address
            )

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.settimeout(timeout)
                sock.bind((local_address, 1025))
                sock.sendto(DISCOVERY_QUERY[4:], (QUERY_TARGET, prt))
            except socket.error:
                raise TPLinkException.SocketError('Discover Socket Error:')
            else:
                try:
                    while True:
                        data, addr = sock.recvfrom(4096)
                        ip, p = addr
                        info = json.loads(protocol.decrypt(data))

                        for key in ('schedule', 'count_down', 'anti_theft'):
                            if (
                                'err_code' in info[key]['get_rules'] and
                                info[key]['get_rules']['err_code'] == -11
                            ):

                                class Device(object):
                                    @staticmethod
                                    def query(**kwargs):
                                        import protocol
                                        return protocol.query(ip, **kwargs)


                                from dtime import DTime
                                time_setter = DTime(Device)
                                time_setter.set()
                                restart = True
                                break

                        info['ip'] = ip
                        info['port'] = port
                        dvcs.append(info)

                except socket.timeout:
                    if not restart:
                        _LOGGER.debug(
                            "Found %d devices on local address %s",
                            len(dvcs),
                            local_address
                        )
                        devices.extend(dvcs)

                except socket.error:
                    _LOGGER.error("Got exception %s")
            finally:
                evt.set()

        events += [threading.Event()]
        t = threading.Thread(target=do, args=(lcl_address, port, events[-1]))
        t.daemon = True
        t.start()

    for event in events:
        event.wait()

    if restart:
        return discover(timeout, port)
    return devices


if __name__ == '__main__':
    for d in discover():
        print json.dumps(d, indent=4)

