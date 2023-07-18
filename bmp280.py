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
        # temp = 0
        # for i in range(size):
        #     temp += int(data[i]) << (8 * i)
        # return temp
        
        # return int.from_bytes(data, 'little', True)
    
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

    def bmp280_compensate_T_int32(self, raw_temp):
        dig_T1 = ustruct.unpack('<H', self.read_register(0x88, 2))[0]
        dig_T2 = ustruct.unpack('<h', self.read_register(0x8A, 2))[0]
        dig_T3 = ustruct.unpack('<h', self.read_register(0x8C, 2))[0]
        print(str(dig_T1) + " " + str(dig_T2) + " " + str(dig_T3))

        # var1 = (((raw_temp>>3) - (dig_T1<<1)) * (dig_T2)) >> 11
        # var2 = (((((raw_temp>>4) - (dig_T1)) * ((raw_temp>>4) - (dig_T1)))>> 12) *(dig_T3)) >> 14
        # t_fine = var1 + var2
        # T = (t_fine * 5 + 128) >> 8
        # return T
    
        # From C API
        var1 = ((raw_temp) / 16384.0 - (dig_T1) / 1024.0) * dig_T2
        var2 = (((raw_temp) / 131072.0 - (dig_T1) / 8192.0) * ((raw_temp) / 131072.0 - (dig_T1) / 8192.0)) * (dig_T3)

        t_fine = int(var1 + var2)       # not used here?
        temperature = (var1 + var2) / 5120.0

        # if (temperature < BMP2_MIN_TEMP_DOUBLE)
        # {
        #     temperature = BMP2_MIN_TEMP_DOUBLE;
        #     rslt = BMP2_W_MIN_TEMP;
        # }

        # if (temperature > BMP2_MAX_TEMP_DOUBLE)
        # {
        #     temperature = BMP2_MAX_TEMP_DOUBLE;
        #     rslt = BMP2_W_MAX_TEMP;
        # }

        return temperature

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