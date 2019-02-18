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
# This software released into the public domain. Anyone is free to copy,
# modify, publish, use, compile, sell, or distribute this software,
# either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, and by any means.


import sys
import socket
import ctypes

from ctypes.wintypes import (
    USHORT,
    BYTE,
    ULONG,
    INT
)


# noinspection PyPep8,PyBroadException
try:
    unicode
except:
    # noinspection PyShadowingBuiltins
    basestring = str

NULL = None
ADDRESS_FAMILY = USHORT
CHAR = ctypes.c_char

ws2_32 = ctypes.windll.ws2_32


# noinspection PyTypeChecker,PyTypeChecker,PyPep8Naming
class sockaddr(ctypes.Structure):
    _fields_ = [
        ('sa_family', ADDRESS_FAMILY),
        ("__pad1", USHORT),
        ("ipv4_addr", BYTE * 4),
        ("ipv6_addr", BYTE * 16),
        ("__pad2", ULONG)
    ]


SOCKADDR = sockaddr
PSOCKADDR = ctypes.POINTER(sockaddr)

WSAStringToAddressW = ws2_32.WSAStringToAddressW
WSAAddressToStringW = ws2_32.WSAAddressToStringW


# noinspection PyPep8Naming
def inet_pton(AddressFamily, AddressString):
    if AddressFamily not in (socket.AF_INET, socket.AF_INET6):
        raise socket.error('unknown address family')

    if isinstance(AddressString, basestring):
        AddressString = ctypes.create_unicode_buffer(AddressString)

    lpProtocolInfo = NULL

    lpAddress = SOCKADDR()
    lpAddress.sa_family = ADDRESS_FAMILY(AddressFamily)
    lpAddressLength = INT(ctypes.sizeof(lpAddress))

    res = WSAStringToAddressW(
        AddressString,
        AddressFamily,
        lpProtocolInfo,
        ctypes.byref(lpAddress),
        ctypes.byref(lpAddressLength)
    )

    if res:
        if AddressFamily == socket.AF_INET:
            return ctypes.string_at(lpAddress.ipv4_addr, 4)
        if AddressFamily == socket.AF_INET6:
            return ctypes.string_at(lpAddress.ipv6_addr, 16)

    raise socket.error(ctypes.FormatError())


# noinspection PyPep8Naming
def inet_ntop(AddressFamily, PackedIP):
    if AddressFamily not in (socket.AF_INET, socket.AF_INET6):
        raise socket.error('unknown address family')

    lpsaAddress = SOCKADDR()
    dwAddressLength = INT(ctypes.sizeof(lpsaAddress))
    lpProtocolInfo = NULL

    lpsaAddress.sa_family = ADDRESS_FAMILY(AddressFamily)

    lpszAddressString = ctypes.create_unicode_buffer(128)
    lpdwAddressStringLength = INT(ctypes.sizeof(lpszAddressString))

    if AddressFamily == socket.AF_INET:
        if len(PackedIP) != ctypes.sizeof(lpsaAddress.ipv4_addr):
            raise socket.error('packed IP wrong length for inet_ntoa')
        ctypes.memmove(lpsaAddress.ipv4_addr, PackedIP, 4)
    elif AddressFamily == socket.AF_INET6:
        if len(PackedIP) != ctypes.sizeof(lpsaAddress.ipv6_addr):
            raise socket.error('packed IP wrong length for inet_ntoa')
        ctypes.memmove(lpsaAddress.ipv6_addr, PackedIP, 16)

    res = WSAAddressToStringW(
        ctypes.byref(lpsaAddress),
        dwAddressLength,
        lpProtocolInfo,
        lpszAddressString,
        ctypes.byref(lpdwAddressStringLength)
    )

    if res == 0:
        return lpszAddressString[:lpdwAddressStringLength.value - 1]

    raise socket.error(ctypes.FormatError())
