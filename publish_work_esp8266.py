from time import sleep
from time import time
from umqtt.simple import MQTTClient
import machine
from machine import Pin, SPI
try:
    import max7219
except Exception as e: print(str(e))

print('in publish max7219')
print('version 20230505 v_0.02')


try:
    display = max7219.SevenSegment(digits=8, scan_digits=4, cs=12, spi_bus=1, reverse=True)
    display.text("ABCDEF")
    display.number(3.14159)
    display.message("Hello World")
    display.clear()
except Exception as e: print(str(e))

print('going to sleep')
sleep(100000)
print('end sleep')