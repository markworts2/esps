from time import sleep
from time import time
from umqtt.simple import MQTTClient
import machine
from machine import Pin, SPI
import max7219

print('in publish max7219')
print('version 20230505 v_0.02')


try:
    display = max7219.SevenSegment(digits=16, scan_digits=8, cs=12, spi_bus=2, reverse=True)
    display.text("ABCDEF")
    display.number(3.14159)
    display.message("Hello World")
    display.clear()
except Exception as e: print(str(e))


sleep(100000)
print('end sleep')