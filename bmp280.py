"""
Library functions in Micropython to run on the RPi Pico.
Lots copied from rtc.py
Sensor is BMP280. Pins:
BMP280 - Pico
SCL - 2
SDA - 3
CSB - 5
SDD - 4
"""

from machine import Pin, SPI
import time

class BMP280:
    def __init__(self, pin):
        self.init(pin)

    def init(self, pin):
        self.spi = SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4), baudrate=2000000, phase=0)
        self.cs = Pin(pin, Pin.OUT, value=1)

    def deinit(self):
        self.spi.deinit()
        self.cs.init(Pin.IN)

    def read_id(self):
        self.cs.value(0)
        self.spi.write(bytes([0xD0]))
        data = self.spi.read(1)
        self.cs.value(1)
        return data

    """
    # Write the command then read size bytes
    def read_bulk(self, command, size):
        self.cs.value(0)
        self.spi.write(bytes([command]))
        data = self.spi.read(size)
        self.cs.value(1)
        return data

    # Written for 0x03 commmand (READ)
    def read_data(self, addr, size):
        self.cs.value(0)
        toWrite = [addr >> 16 & 0xFF, addr >> 8 & 0xFF, addr & 0xFF]
        self.spi.write(bytes([0x03] + toWrite))
        data = self.spi.read(size)
        self.cs.value(1)
        return data
    """