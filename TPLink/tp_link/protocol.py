"""
Implementation of the TP-Link Smart Home Protocol

Encryption/Decryption methods based on the works of
Lubomir Stroetmann and Tobias Esser

https://www.softscheck.com/en/reverse-engineering-tp-link-hs110/
https://github.com/softScheck/tplink-smartplug/

which are licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

import json
import socket
import struct
import _LOGGER
import TPLinkException

INITIALIZATION_VECTOR = 171
DEFAULT_PORT = 9999
DEFAULT_TIMEOUT = 5


POLL_QUERY = dict(
    system=dict(get_sysinfo=None),
    emeter=dict(get_realtime=None, get_vgain_igain=None),
    schedule=dict(get_rules=None),
    count_down=dict(get_rules=None),
    anti_theft=dict(get_rules=None),
    time=dict(get_time=None, get_timezone=None),
    cnCloud=dict(get_info=None),
    lightingservice=dict(get_light_details=None)
)


def poll(host):
    _, response = query(host, **POLL_QUERY)

    for key, value in response.items()[:]:
        if isinstance(value, dict):
            if len(value.keys()) == 1 and value.keys()[0].startswith('get_'):
                response[key] = value[value.keys()[0]]

    return response


def query(ip, port=DEFAULT_PORT, **kwargs):

    """
    Request information from a TP-Link SmartHome Device and return the
    response.

    :param str ip: ip address of the device
    :param int port: port on the device (default: 9999)
    :param request: command to send to the device (can be either dict or
    json string)
    :return:
    """

    data = json.dumps(kwargs)

    _LOGGER.debug(">> (%i) %s", len(data), data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((ip, port))
    except socket.error:
        raise TPLinkException.SocketError("Socket Connection Error:")

    sock.send(encrypt(data))

    buf = bytes()
    # Some devices send responses with a length header of 0 and
    # terminate with a zero size chunk. Others send the length and
    # will hang if we attempt to read more data.
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

    try:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except socket.error:
        pass

    if not len(buf):
        raise TPLinkException.CorruptedDataError('No Data Received')

    response = decrypt(buf[4:])
    _LOGGER.debug("<< (%i) %s", len(response), response)

    return json.loads(response)


def encrypt(request):
    key = INITIALIZATION_VECTOR
    buf = bytearray(struct.pack(">I", len(request)))

    for char in request:
        encoded = key ^ ord(char)
        key = encoded
        buf.append(encoded)

    return buf


def decrypt(data):

    key = INITIALIZATION_VECTOR
    buf = ''

    data = data.decode('latin-1')

    for char in data:
        buf += chr(key ^ ord(char))
        key = ord(char)

    return buf
