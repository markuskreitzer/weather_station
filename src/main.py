import machine
import urequests
from machine import Pin, SoftI2C
import network, time
import BME280

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)    #initializing the I2C method
addresses = i2c.scan()

if len(addresses) > 0:
    i2c_address = addresses[0]
    print(f'Found I2C device: {i2c_address}')
else:
    raise Exception("No I2C device detected")

HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = 'M7P072PSZG7B7VQB'

UPDATE_TIME_INTERVAL = 120000  # in ms
last_update = time.ticks_ms() 

ssid='braaispice'
password='mygrillisabraai2019!!'

# Configure ESP32 as Station
sta_if=network.WLAN(network.STA_IF)
sta_if.active(True)

if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        pass

print('network config:', sta_if.ifconfig()) 

while True: 
    if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL: 
        print(time.ticks_ms(), last_update, UPDATE_TIME_INTERVAL)
        bme = BME280.BME280(i2c=i2c, address=i2c_address)
        temperature = bme.temperature
        humidity = bme.humidity
        pressure = bme.pressure
        wind_direction = 0
        wind_speed = 0
        precipitation = 0
        bme_readings = {'field1':temperature[0], 'field2':pressure[0], 'field3':humidity[0], 'field4': wind_direction, 'field5': wind_speed, 'field6': precipitation}
        req = urequests.post('https://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY,json=bme_readings,headers=HTTP_HEADERS)
        print(req.status_code)
        print(req.text)
        req.close()
        print(bme_readings) 
        last_update = time.ticks_ms() 
