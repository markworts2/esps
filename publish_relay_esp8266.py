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
print('publish relay')

# create an input pin on pin 14
pp = 14
print(pp)
p14 = Pin(pp, Pin.IN)

# set the value low then high - testing when power on or off
pint27 = 27 # Intervalue of pin
p27 = Pin(pint27, Pin.OUT) # initiate pin as output
print ("boot state")
print('turning off')
p27.value(0)
sleep(20)
print('Turning on')
p27.value(1)
print('on - sleeping')
sleep(20)
print('Sleep over')

SERVER = '192.168.86.248'  # MQTT Server Address (Change to the IP address of your Pi)
CLIENT_ID = 'ESP32_DHT22_Sensor'
TOPIC = b'temp_humidity'
#rtc = machine.RTC()
#adc = ADC(0)  #get the ADC0 pin reading (Analogue to digital pin)

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

#send the 14 pin out reading
print ('report pin14')
try:
   msg = date_str +  ",display," + str(p14)
   print (msg)
   client.publish(TOPIC,str(msg))  # Publish P14 which is the water meter reading
except Exception as e: print(str(e))

print('4')
ds_pin = machine.Pin(4)
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
