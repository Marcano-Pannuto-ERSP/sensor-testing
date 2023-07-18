# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText 2023 Kristin Ebuengan
# SPDX-FileCopyrightText 2023 Melody Gill
# SPDX-FileCopyrightText 2023 Gabriel Marcano

from machine import Pin
from bmp280 import *
import time
import ustruct

# first bring CSB low to select SPI
cs = Pin(5, Pin.OUT, value=0)

# make BMP280 object
sensor = BMP280(5)
print(hex(sensor.read_id()[0]))
print(hex(sensor.read_register(0xD0, 1)[0]))
i = 0
data = 0
while(i < 3):
    data = sensor.get_adc_temp()
    data2 = sensor.get_adc_pressure()
    print(data)
    print(data2)
    time.sleep(0.05)
    i += 1
print(hex(ustruct.unpack('<H', sensor.read_register(0xF3, 2))[0]))
print(sensor.bmp280_compensate_T_int32(data))
print(sensor.bmp280_compensate_P_double(data2, data))