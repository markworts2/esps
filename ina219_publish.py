from time import sleep
from time import time
from umqtt.simple import MQTTClient
import machine
from dht import DHT22
from ina219 import INA219
import onewire, ds18x20
from struct import unpack
from machine import Pin
from machine import I2C
from machine import ADC
print('end of imports')
print('version 20220425_v_w0.1')

SHUNT_OHMS = 0.1

ina = INA219()
reading = ina.read()
print (reading[0],reading[1],reading[2])
reading2 = ina.readI()
print (reading2)
reading3 = ina.readW()
print (reading3)


SERVER = '192.168.86.248'  # MQTT Server Address (Change to the IP address of your Pi)
CLIENT_ID = 'ESP32_DHT22_Sensor'
TOPIC = b'temp_humidity'
rtc = machine.RTC()

date_str = "{2:02d}/{1:02d}/{0:4d} {4:02d}:{5:02d}".format(*rtc.datetime())

# connect to the mosquito server
print('Connecting to MQTT')
client = MQTTClient(CLIENT_ID, SERVER)
try:
   client.connect()   # Connect to MQTT broker
except IndexError:
   print ('index error connecting to mosquito server')

#send date and reading
try:
   msg = date_str + ",IV," + str(reading[0]) + "," + str(reading[1])
   client.publish(TOPIC,str(msg))  # Publish voltage data to MQTT topic
except Exception as e: print(str(e))
sleep(5)
