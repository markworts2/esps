from time import sleep
from time import time
from umqtt.simple import MQTTClient
import machine
from dht import DHT22
import onewire, ds18x20
from struct import unpack
from machine import Pin
from machine import ADC
print('end of imports')
print('version 20220329_v_w0.1')

# create an output pin on pin #0
# pp = 4
# print(pp)
# p0 = Pin(pp, Pin.IN)

# set the value low then high
#print('off')
#p0.value(0)
#sleep(20)
#print('on')
#p0.value(1)
#sleep(10)
#print('off')
#p0.value(0)

SERVER = '192.168.86.248'  # MQTT Server Address (Change to the IP address of your Pi)
CLIENT_ID = 'ESP32_DHT22_Sensor'
TOPIC = b'temp_humidity'
rtc = machine.RTC()
adc = ADC(0)  #get the ADC0 pin reading (Analogue to digital pin)

date_str = "{2:02d}/{1:02d}/{0:4d} {4:02d}:{5:02d}".format(*rtc.datetime())

# connect to the mosquito server
print('Connecting to MQTT')
client = MQTTClient(CLIENT_ID, SERVER)
try:
   client.connect()   # Connect to MQTT broker
except IndexError:
   print ('index error connecting to mosquito server')

#send the ADC0 pin out reading
print ('report adc0')
try:
   vadc = adc.read()
   msg = date_str +  ",power," + str(vadc)
   print (msg)
   client.publish(TOPIC,str(msg))  # Publish voltage data to MQTT topic
except Exception as e: print(str(e))

print('2')
ds_pin = machine.Pin(2)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
print('Found DS devices: ', roms)

try:
    ds_sensor.convert_temp()
    sleep(1)
    for rom in roms:
      try:
        print ('rom :', rom)
#        print ('rom0 :', rom[0])
#        print ('rom1 :', rom[1])
#        print ('rom2 :', rom[2])
        msg = date_str +  "," + str(hex(unpack('<q', rom))) + "," + str(ds_sensor.read_temp(rom))
        client.publish(TOPIC, msg)  # Publish sensor data to MQTT topic
        print(msg)
      except:
        print('error')
#        client.publish(TOPIC, 'error')
except OSError:
    d = time()
    msg = (b'{}'.format(d))
    print('Failed to read sensor.')
    client.publish(TOPIC,msg)
sleep(5)
