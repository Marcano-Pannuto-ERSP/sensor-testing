from machine import Pin
from bmp280 import *

# first bring CSB low to select SPI
cs = Pin(5, Pin.OUT, value=0)

# make BMP280 object
sensor = BMP280(5)
print(hex(sensor.read_id()[0]))
print(sensor.get_adc_temp())