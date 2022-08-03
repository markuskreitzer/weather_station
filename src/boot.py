try:
  import usocket as socket
except:
  import socket
from time import sleep
from machine import Pin
from machine import SoftI2C as I2C
import network
import esp
esp.osdebug(None)

import gc
gc.collect()

# ESP32 - Pin assignment
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)

# ESP8266 - Pin assignment
#i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)

addresses = i2c.scan()
if len(addresses) > 0:
    i2c_address = addresses[0]
    print(f'Found I2C device: {i2c_address}')
else:
    raise Exception("No I2C device detected")

# Add your SSID and password for wifi network here.
ssid = 'xxxxx'
password = 'xxxxxx'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

