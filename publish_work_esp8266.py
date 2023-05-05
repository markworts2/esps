from time import sleep
from time import time
from umqtt.simple import MQTTClient
import machine
from machine import Pin, SPI
import max7219

print('in publish max7219')
print('version 20230505 v_0.01')

spi = SPI(1, baudrate=10000000)
screen = max7219.Max7219(64, 8, spi, Pin(12))
screen.text('12345678', 0, 0, 1)
screen.show()

sleep(100000)
print('end sleep')