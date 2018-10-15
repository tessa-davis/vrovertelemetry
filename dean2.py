import time
import sys
import datetime
import Adafruit_BMP.BMP085 as BMP085
from influxdb import InfluxDBClient
import argparse
import socket
import time
import subprocess
import os
CARBON_SERVER = '192.168.11.200'
CARBON_PORT = 2003


host = "192.168.11.200"
port = 8086
user = "fevr11_t"
password = "fevr11_t"
dbname = "sensor_data"
#interval = 60
interval = 1

client = InfluxDBClient (host, port, user, password, dbname)

sensor = BMP085.BMP085()

#sensor_gpio = 3

measurement = "fevr11_t-bmp085"
location = "mars"

try:
  while True:
    #temperature = Adafruit_BMP.BMP085.read_retry(Adafruit_BMP.BMP08, 3)
    #temperature = {0:0.2f}.format(sensor.read_temperature())
    temperature = sensor.read_temperature()
    pressure = sensor.read_pressure()
    altitude = sensor.read_altitude()
    sealevel_pressure = sensor.read_sealevel_pressure()
    print(sensor.read_temperature())
    iso = time.ctime()
    data = [
    {
      "measurement": measurement,
        "tags": {
          "location": location,
        },
        "time": iso,
        "fields": {
          "temperature": temperature,
          "pressure": pressure,
          "altitude": altitude,
          "sealevel_pressure": sealevel_pressure
        }
      }
    ]
    client.write_points(data)
    oscommandtesttemp = "echo 'mars.environmental.temp.1s '"+str(temperature)+"  | nc -q0 192.168.11.200 2003"
    oscommandtestpress = "echo 'mars.environmental.pressure.1s '"+str(pressure)+"  | nc -q0 192.168.11.200 2003"
    oscommandtestalt = "echo 'mars.environmental.altitude.1s '"+str(altitude)+"  | nc -q0 192.168.11.200 2003"
    oscommandtestslpress = "echo 'mars.environmental.sealevel_pressure.1s '"+str(sealevel_pressure)+"  | nc -q0 192.168.11.200 2003"
    os.system(oscommandtesttemp)
    os.system(oscommandtestpress) 
    os.system(oscommandtestalt)
    os.system(oscommandtestslpress)
    print("hello")
    print(data)
    time.sleep(interval)

except KeyboardInterrupt:
  pass
