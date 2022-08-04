from time import sleep
from time import time
from umqtt.simple import MQTTClient
import machine
from dht import DHT22
import onewire, ds18x20
from struct import unpack
from machine import Pin,ADC

#Real Time Cloud initialisation
rtc = machine.RTC()

p14 = Pin(14, Pin.IN) #set pin 14 to read in

#Create Analogue to Digital for port 34
pot = ADC(Pin(39))
pot.atten(ADC.ATTN_11DB)       #Full range: 3.3v

pot_value = {}

iterations = 1000

#Test loop to print the ADC value

while True:
  count = 0recording_time = rtc.datetime()
  average_vol = 0
  min_vol  = 10000
  while True:
    vol = pot.read()
    if vol < min_vol:min_vol=vol
    average_vol = average_vol + vol
    count += 1
    sleep(0.01)
    if count > iterations:break


  average_vol = average_vol / count
  date_str = "{2:02d}/{1:02d}/{0:4d} {4:02d}:{5:02d}".format(recording_time)
  print(date_str,min_vol,average_vol)
  
# set the value low then high - testing when power on or off
# this can turn on and off power to moisture as it goes geen if always on
pint27 = 27 # Integer value of pin
p27 = Pin(pint27, Pin.OUT) # initiate pin as output
print ("boot state")
print('Turning on to take reading')
p27.value(1)
print('on')
sleep(10) #give change for meter to turn on and create a proper reading



#MQQT connection 
SERVER = '192.168.86.248'  # MQTT Server Address (Change to the IP address of your Pi)
CLIENT_ID = 'ESP32_DHT22_Sensor'
TOPIC = b'temp_humidity'



print('Connecting to MQTT')
client = MQTTClient(CLIENT_ID, SERVER)
try:
   client.connect()   # Connect to MQTT broker
except IndexError:
   print ('index errort')

#read p14 the plan water sensor and push to MQQT
try:
        date_str = "{2:02d}/{1:02d}/{0:4d} {4:02d}:{5:02d}".format(*rtc.datetime())
        msg = date_str +  "," + str('p14') + "," + str(p14.value())
        client.publish(TOPIC, msg)
        print (msg)
except:
        print('Error')

print('turn off')
p27.value(0)

ds_pin = machine.Pin(21)
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
