from time import sleep
import machine
from machine import Pin

def http_get(url):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    sleep(2)
    ret = ""
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            ret = ret + str(data, 'utf8')
#            print('.')
#            print (str(data, 'utf8'), end='')
        else:
            break
    s.close()
    return (ret)

data = http_get('http://192.168.86.248/display_status')

print('response')
desired_state = data[-2]
print (desired_state)

#do the pin change stuff
#set the pin number, move turn on pin unitl after check as it changed stat turning on lights
pp = 14

while desired_state == 'n':
  print('lights on')
  pina = Pin(pp, Pin.OUT)
  pina.value(0)  #pull down to turn on
  sleep(15)
  data = http_get('http://192.168.86.248/display_status')
  print('loop response')
  desired_state = data[-2]
  print (desired_state)


print('exit check html')
