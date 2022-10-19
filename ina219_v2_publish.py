from time import sleep
from time import time
from umqtt.simple import MQTTClient
import machine
from dht import DHT22
from ina219v2 import INA219
import onewire, ds18x20
from struct import unpack
from machine import Pin
from machine import I2C
from machine import ADC
print('end of imports')
print('version 20221019_v_ina0.2')

SHUNT_OHMS = 0.1
I2C_INTERFACE_NO = 2

ina = INA219(SHUNT_OHMS, I2C(I2C_INTERFACE_NO))
ina.configure()
print("Bus Voltage: %.3f V" % ina.voltage())
print("Current: %.3f mA" % ina.current())
print("Power: %.3f mW" % ina.power())

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
