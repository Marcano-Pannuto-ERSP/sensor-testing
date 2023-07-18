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
import ustruct

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
    
    def read_register(self, addr, size):
        self.cs.value(0)
        addr |= 0x80
        self.spi.write(bytes([addr]))
        data = self.spi.read(size)
        self.cs.value(1)
        return data
    
    # Get the temperature from the registers
    def get_adc_temp(self):
        self.cs.value(0)

        # take out of sleep mode
        # set temp oversampling
        activate = 0b00100001

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
    
    def get_adc_pressure(self):
        self.cs.value(0)

        # take out of sleep mode
        # set pressure oversampling
        activate = 0b00000101

        # write pressure sampling to the register
        addr = 0xF4 & 0x7F
        self.spi.write(bytes([addr, activate]))
        self.cs.value(1)

        self.cs.value(0)
        self.spi.write(bytes([0xF7]))
        data = self.spi.read(3)
        self.cs.value(1)
        print([hex(int(x)) for x in data])

        # return data
        pressure = (int(data[0]) << 12) + (int(data[1]) << 4) + (int(data[2]) >> 4)
        return pressure

    # Accuracy of +- 1 celsius
    def bmp280_compensate_T_int32(self, raw_temp):
        dig_T1 = ustruct.unpack('<H', self.read_register(0x88, 2))[0]
        dig_T2 = ustruct.unpack('<h', self.read_register(0x8A, 2))[0]
        dig_T3 = ustruct.unpack('<h', self.read_register(0x8C, 2))[0]
        print(str(dig_T1) + " " + str(dig_T2) + " " + str(dig_T3))
    
        # From C API
        var1 = ((raw_temp) / 16384.0 - (dig_T1) / 1024.0) * dig_T2
        var2 = (((raw_temp) / 131072.0 - (dig_T1) / 8192.0) * ((raw_temp) / 131072.0 - (dig_T1) / 8192.0)) * (dig_T3)

        temperature = (var1 + var2) / 5120.0

        return temperature