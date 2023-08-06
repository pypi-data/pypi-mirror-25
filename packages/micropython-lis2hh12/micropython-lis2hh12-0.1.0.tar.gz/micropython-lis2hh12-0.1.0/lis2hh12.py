"""
MicroPython I2C driver for LIS2HH12 3-axis accelerometer
"""

import utime
import ustruct
from machine import I2C, Pin

_TEMP_L = const(0x0b)
_TEMP_H = const(0x0c)
_WHO_AM_I = const(0x0f)
_CTRL1 = const(0x20)
_CTRL2 = const(0x21)
_CTRL3 = const(0x22)
_CTRL4 = const(0x23)
_CTRL5 = const(0x24)
_CTRL6 = const(0x25)
_CTRL7 = const(0x26)
_OUT_X_L = const(0x28)
_OUT_X_H = const(0x29)
_OUT_Y_L = const(0x2a)
_OUT_Y_H = const(0x2b)
_OUT_Z_L = const(0x2c)
_OUT_Z_H = const(0x2d)

# CTRL1
_ODR_MASK = const(0b01110000)
ODR_OFF = const(0b00000000)
ODR_50HZ = const(0b00100000)
ODR_100HZ = const(0b01100000)
ODR_200HZ = const(0b01000000)

# CTRL4
_FS_MASK = const(0b00110000)
FS_2G = const(0b00000000)
FS_4G = const(0b00100000)
FS_8G = const(0b00110000)

_SO_2G = const(61)
_SO_4G = const(122)
_SO_8G = const(244)

class LIS2HH12:
    def __init__(self, i2c = None, address = 0x1e, odr = ODR_100HZ, fs = FS_2G):
        if i2c is None:
            self.i2c = I2C(scl=Pin(26), sda=Pin(25))
        else:
            self.i2c = i2c

        self.address = address
        self._odr(odr)
        self._fs(fs)

    def read_raw(self):
        x = self._register_word(_OUT_X_L)
        y = self._register_word(_OUT_Y_L)
        z = self._register_word(_OUT_Z_L)
        return (x, y, z)

    def read(self):
        x = self._register_word(_OUT_X_L) * self._so / 1000000
        y = self._register_word(_OUT_Y_L) * self._so / 1000000
        z = self._register_word(_OUT_Z_L) * self._so / 1000000
        return (x, y, z)

    def whoami(self):
        return self._register_char(_WHO_AM_I)

    def _register_word(self, register, value=None):
        if value is None:
            data = self.i2c.readfrom_mem(self.address, register, 2)
            return ustruct.unpack("<h", data)[0]
        data = ustruct.pack("<h", value)
        self.i2c.writeto_mem(self.address, register, data)

    def _register_char(self, register, value=None):
        if value is None:
            return self.i2c.readfrom_mem(self.address, register, 1)[0]
        data = ustruct.pack("<b", value)
        self.i2c.writeto_mem(self.address, register, data)

    def _fs(self, value = None):
        if value is None:
            return None # TODO
        char = self._register_char(_CTRL4)
        char &= ~_FS_MASK # clear FS bits
        char |= value
        self._register_char(_CTRL4, char)

        # Store the sensitivity multiplier
        if FS_2G == value:
            self._so = _SO_2G
        elif FS_4G == value:
            self._so = _SO_4G
        elif FS_8G == value:
            self._so = _SO_8G

    def _odr(self, value = None):
        if value is None:
            return None # TODO
        char = self._register_char(_CTRL1)
        char &= ~_ODR_MASK # clear ODR bits
        char |= value
        self._register_char(_CTRL1, char)
