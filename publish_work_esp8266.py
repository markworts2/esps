from time import sleep
from time import time
from umqtt.simple import MQTTClient
import machine
from machine import Pin, SPI
import max7219

spi = SPI(1, baudrate=10000000)
screen = max7219.Max7219(64, 8, spi, Pin(15))
screen.text('ABCDEFGH', 0, 0, 1)
screen.show()