from time import sleep
from time import time
from umqtt.simple import MQTTClient
import machine
from dht import DHT22
import onewire, ds18x20
from struct import unpack
from machine import Pin

print ('dht_publish_water_esp32.py  v26/06/24 07:43')


p4 = Pin(4, Pin.OUT) #power pin
p5 = Pin(5, Pin.IN) #read water pin
adc = machine.ADC(0) #read water analogue pin

ds_pin = machine.Pin(2)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))



#connect to mqqt
SERVER = '192.168.86.248'  # MQTT Server Address (Change to the IP address of your Pi)
CLIENT_ID = 'ESP32_DHT22_Sensor'
TOPIC = b'temp_humidity'
rtc = machine.RTC()

print('Connecting to MQTT')
client = MQTTClient(CLIENT_ID, SERVER)
try:
   client.connect()   # Connect to MQTT broker
except IndexError:
   print ('index error: can not connect to MQQT')
   
date_str = "{2:02d}/{1:02d}/{0:4d} {4:02d}:{5:02d}".format(*rtc.datetime())

#print(rtc.datetime())
date_t=rtc.datetime()
print(date_t[4],date_t[4]/6,int(date_t[4]/6))
if date_t[4]/6 == int(date_t[4]/6):
        print('turn on power pin 4')
        p4.value(1) #turn on the power pin
        sleep(10)
        print('read pin 5 the sensor pin')
        dreading = p5.value()
        areading = adc.read()
        p4.value(0)
        print('turned off power pin')

        # push to MQQT
        msg = date_str +  "," + str('water_p5') + "," + str(dreading)
        try:
                client.publish(TOPIC, msg)
                print (msg)
        except:
                print("publish binary failed")
                print (msg)

                
        msg = date_str +  "," + str('water_p3') + "," + str(areading)
        try:
                client.publish(TOPIC, msg)
        except:
                print("publish analogue failed")
                print (msg)

roms = ds_sensor.scan() #return
print('Found DS devices: ', roms)


try:
        ds_sensor.convert_temp()
        sleep(1)
        for rom in roms:
                msg = date_str +  "," + str(hex(unpack('<q', rom))) + "," + str(ds_sensor.read_temp(rom))
                try:
                        print("Client connect")
                        client.connect()   # Connect to MQTT broker
                except IndexError:
                        print ('index error: can not connect to MQQT')
                client.publish(TOPIC, msg)  # Publish sensor data to MQTT topic
                print(msg)
except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print('error readin DHT')
print('hi')
sleep(10)