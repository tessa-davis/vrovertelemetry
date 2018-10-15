import time
import sys
import datetime
import Adafruit_BMP.BMP085 as BMP085
from influxdb import InfluxDBClient

host = "192.168.11.200"
port = 8086
user = "fevr11_t"
password = "fevr11_t"
dbname = "sensor_data"
#interval = 60
interval = 5

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
    os.system(echo mars.environmental.temp.1m temperature `date +%s` | nc 192.168.11.200 2003)
    print("hello")
    print(data)
    time.sleep(interval)

except KeyboardInterrupt:
  pass
