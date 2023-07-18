from machine import Pin
from bmp280 import *
import time
import ustruct

# first bring CSB low to select SPI
cs = Pin(5, Pin.OUT, value=0)

# make BMP280 object
sensor = BMP280(5)
print(hex(sensor.read_id()[0]))
print(ustruct.unpack('<H', sensor.read_register(0xD0, 1))[0])
i = 0
data = 0
while(i < 3):
    data = sensor.get_adc_temp()
    print(data)
    time.sleep(0.05)
    i += 1
print(ustruct.unpack('<H', sensor.read_register(0xF3, 2))[0])
print(sensor.bmp280_compensate_T_int32(data))