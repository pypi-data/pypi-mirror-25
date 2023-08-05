#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2017 Matthew Pare (paretech@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from struct import pack
from struct import unpack
from datetime import datetime
from datetime import timezone


def datetime_to_bytes(value):
    """Return bytes representing UTC time in microseconds."""
    return pack('>Q', int(value.timestamp() * 1e6))


def bytes_to_datetime(value):
    """Return datetime from microsecond bytes."""
    return datetime.fromtimestamp(bytes_to_int(value)/1e6, tz=timezone.utc)


def bytes_to_int(value, signed=False):
    """Return integer given bytes."""
    return int.from_bytes(bytes(value), byteorder='big', signed=signed)


def int_to_bytes(value, length=1, signed=False):
    """Return bytes given integer"""
    return int(value).to_bytes(length, byteorder='big', signed=signed)


def ber_decode(value):
    """Return decoded BER length as integer given bytes."""
    if bytes_to_int(value) < 128:
        if len(value) > 1:
            raise ValueError

        # Return BER Short Form
        return bytes_to_int(value)
    else:
        if len(value) != (value[0] - 127):
            raise ValueError

        # Return BER Long Form
        return bytes_to_int(value[1:])


def ber_encode(value):
    """Return encoded BER length as bytes given integer."""
    if value < 128:
        # BER Short Form
        return int_to_bytes(value)
    else:
        # BER Long Form
        byte_length = ((value.bit_length() - 1) // 8) + 1

        return int_to_bytes(byte_length + 128) + int_to_bytes(value, length=byte_length)


def bytes_to_str(value):
    """Return UTF-8 formatted string from bytes object."""
    return bytes(value).decode('UTF-8')


def str_to_bytes(value):
    """Return bytes object from UTF-8 formatted string."""
    return bytes(str(value), 'UTF-8')


def hexstr_to_bytes(value):
    """Return bytes object and filter out formatting characters from a string of hexadecimal numbers."""
    return bytes.fromhex(''.join(filter(str.isalnum, value)))


def bytes_to_hexstr(value, start='', sep=' '):
    """Return string of hexadecimal numbers separated by spaces from a bytes object."""
    return start + sep.join(["{:02X}".format(byte) for byte in bytes(value)])


def bytes_to_float(value, _domain, _range):
    """Convert the fixed point value self.value to a floating point value."""
    x1, x2 = _domain

    length = int((x2 - x1 - 1).bit_length() / 8)
    if length != len(value):
        raise ValueError

    y1, y2 = _range
    m = (y2 - y1) / (x2 - x1)

    x = bytes_to_int(value, signed=any((i < 0 for i in _range)))

    # Return y given x
    return m * (x - x1) + y1


def float_to_bytes(value, _domain, _range):
    """Convert the fixed point value self.value to a floating point value."""
    x1, x2 = _domain
    y1, y2 = _range
    m = (y2 - y1) / (x2 - x1)
    y = value

    length = int((x2 - x1 - 1).bit_length() / 8)
    signed = any((i < 0 for i in _range))
    x = round((1 / m) * (y - y1) + x1)

    # Return x given y
    return int_to_bytes(x, length, signed)


def packet_checksum(data):
    """Return two byte checksum from a SMPTE ST 336 KLV structured bytes object."""
    length = len(data) - 2
    word_size, mod = divmod(length, 2)

    words = sum(unpack(">{:d}H".format(word_size), data[0:length - mod]))

    if mod:
        words += data[length - 1] << 8

    return pack('>H', words & 0xFFFF)
