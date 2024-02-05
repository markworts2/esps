from time import sleep
from time import time
from umqtt.simple import MQTTClient
import machine
from machine import Pin, SPI
try:
    import max7219
except Exception as e: print(str(e))

print('in publish max7219')
print('version 20240205 v_0.02')

DIN = 13
CS = 12
CLK = 14

pdin = Pin(DIN, Pin.OUT)
pcs = Pin(CS, Pin.OUT)
pclk = Pin(CLK, Pin.OUT)


try:
    display = max7219.SevenSegment(digits=8, scan_digits=4, cs=5, spi_bus=1, reverse=False)
    print("ABCDEF")
    display.text("ABCDEF")
    sleep(10)
    print('3.14159')
    display.number(3.14159)
    sleep(10)
    print('Hello World')
    display.message("Hello World")
    sleep(10)
    display.clear()
except Exception as e: print(str(e))

print('going to sleep')
sleep(10)
print('end sleep')