from machine import Pin
from bmp280 import *
import time

# first bring CSB low to select SPI
cs = Pin(5, Pin.OUT, value=0)

# make BMP280 object
sensor = BMP280(5)
print(hex(sensor.read_id()[0]))
while(True):
    print(sensor.get_adc_temp())
    time.sleep(1)