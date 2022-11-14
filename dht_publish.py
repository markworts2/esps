from time import sleep
from time import time
from umqtt.simple import MQTTClient
import machine
from dht import DHT22
import onewire, ds18x20
from struct import unpack
from machine import Pin
print ("dht_publish v221114_1 ds_pin 4")

p14 = Pin(14, Pin.IN)

SERVER = '192.168.86.248'  # MQTT Server Address (Change to the IP address of your Pi)
CLIENT_ID = 'ESP32_DHT22_Sensor'
TOPIC = b'temp_humidity'
rtc = machine.RTC()

print('Connecting to MQTT')
client = MQTTClient(CLIENT_ID, SERVER)
try:
   client.connect()   # Connect to MQTT broker
except IndexError:
   print ('index errort')


try:
        date_str = "{2:02d}/{1:02d}/{0:4d} {4:02d}:{5:02d}".format(*rtc.datetime())
        msg = date_str +  "," + str('p14') + "," + str(p14.value())
        client.publish(TOPIC, msg)
except:
        print('Error')

ds_pin = machine.Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
print('Found DS devices: ', roms)

try:
    ds_sensor.convert_temp()
    sleep(1)
    for rom in roms:
      try:
        date_str = "{2:02d}/{1:02d}/{0:4d} {4:02d}:{5:02d}".format(*rtc.datetime())
        print ('rom :',rom)
        msg = date_str +  "," + str(unpack('<H', rom)[0]) + "," + str(ds_sensor.read_temp(rom))
        client.publish(TOPIC, msg)  # Publish sensor data to MQTT topic
        print(msg)
      except:
        client.publish(TOPIC, '')
except OSError:
    d = time()
    msg = (b'{}'.format(d))
    print('Failed to read sensor.')
    client.publish(TOPIC,msg)
sleep(5)
