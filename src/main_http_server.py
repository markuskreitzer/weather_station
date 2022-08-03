import re

def web_page():
  bme = BME280.BME280(i2c=i2c, address=i2c_address)
  with open('index.html') as fh:
      return fh.read()

def json():
  bme = BME280.BME280(i2c=i2c, address=i2c_address)
  #return f'\{\"temp\": {bme.temperature}, \"hum\": {bme.humidity}, \"pres\": {bme.pressure}\}'
  return "{\"temp\": \"%s\", \"hum\": \"%s\", \"pres\": \"%s\"}" % (bme.temperature, bme.humidity, bme.pressure)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    conn.send('HTTP/1.1 200 OK\n')
    
    if re.search('GET /json', request):
        response = json()
        conn.send('Content-Type: application/json\n')
    else:
        response = web_page()
        conn.send('Content-Type: text/html\n')

    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')

