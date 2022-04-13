#!/bin/sh

sleep 60
mosquitto_sub -h 192.168.86.248 -t "temp_humidity" >> /var/www/html/temp_d.csv
  pass
