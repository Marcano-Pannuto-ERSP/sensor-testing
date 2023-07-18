# sensor-testing

## Read Temperature and Pressure
Uses a Raspberry Pi Pico to read the temperature/pressure from a BMP280 using SPI.

`bmp280.py` contains functions to initialize the sensor and get temperature/pressure and calculate the temperature/pressure. 

**NOTICE:** Before using any of the functions you will have to upload `bmp280.py` on the Rasberry Pi Pico and bring the CSB pin low to select SPI.

`bmp280-testing.py` contains a test example of how to use the functions.

Here is the datasheet of the flash chip for more details: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp280-ds001.pdf

**NOTICE:** Temperature reading has a +- 1 celsius accuracy

**Pins:**
- BMP280 - Pico
- SCL - 2
- SDA - 3
- CSB - 5
- SDD - 4