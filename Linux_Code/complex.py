from bluetooth import *
from influxdb import InfluxDBClient
import time
import threading
import socket

#bluetooth ready
bd_addr="00:18:E5:04:12:DC"

port=1
sock=BluetoothSocket(RFCOMM)
sock.connect((bd_addr, port))

print ("Finished")
power = ""

#connect DB
host='192.168.0.29' #my Ubuntu IP
port=8086
user="yesol"
password="k1010910"
dbname=“betadb"
interval=10

#Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)

measurement=“house"
location="plug1"
ip="192.168.0.29"

def message(): #message include order
	print ("Main Thread")
	sock_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_s.bind((ip, 8080))

	while True:
		data, addr = sock_s.recvfrom(200)
		sock.send(data)
		print("send message:", data.decode())
		print("Send Client IP:", addr[0])
		print("Send Client Port:", addr[1])

t = threading.Thread(target=message)
t.start()

#receive power from arduino & insert power to DB
try:
	while True:
		power_c = sock.recv(1)
		if power_c.decode() != ‘/’:
			power += str(power_c.decode())
		elif len(power) > 0:
			print ('Receive', power)
			sock.send("OK")

		iso = time.ctime()
		data = [
		{
			"measurement": measurement,
			"tags": {
				"location": location
			},
			"time": iso,
			"fields": {
				"Power" : float(power),
				"IP" : ip
			}
		}
		]

		# Send the JSON data to InfluxDB
		client.write_points(data)

		# Wait until it's time to query again...
		time.sleep(interval)

		power = ""
except KeyboardInterrupt:
    pass
