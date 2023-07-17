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
    
    # Get the temperature from the registers
    def get_adc_temp(self):
        self.cs.value(0)

        # take out of sleep mode
        # set temp oversampling
        activate = 0b00100011

        # write temp sampling to the register
        addr = 0xF4 & 0x7F
        self.spi.write(bytes([addr, activate]))
        self.cs.value(1)

        self.cs.value(0)
        self.spi.write(bytes([0xFA]))
        data = self.spi.read(3)
        self.cs.value(1)
        print([hex(int(x)) for x in data])

        # return data
        temp = (int(data[0]) << 12) + (int(data[1]) << 4) + (int(data[2]) >> 4)
        return temp

    def bmp280_compensate_T_int32 (adc_T):
        var1 = ((((adc_T>>3) - (dig_T1<<1))) * (dig_T2)) >> 11
        var2 = (((((adc_T>>4) - (dig_T1)) * ((adc_T>>4) - (dig_T1)))>> 12) *(dig_T3)) >> 14
        t_fine = var1 + var2
        T = (t_fine * 5 + 128) >> 8
        return T

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