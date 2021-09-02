<send_db.py>

import time
from influxdb import InfluxDBClient

host='192.168.0.30'#my Ubuntu IP
port=8086
user="yesol"
password="k1010910"
dbname="testdb"
interval=10

#Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)

measurement="house"
location="plug10"

try:
	while True:
		Power=30000
		Iso = time.ctime()
		data = [
		{
		"measurement": measurement,
			"tags": {
				"location": location,
			},
			"time": iso,
			"fields": {
				"Power" : Power
			}
		}
		]

	# Send the JSON data to InfluxDB
	client.write_points(data)
	# Wait until it's time to query again...
	time.sleep(interval)
 
except KeyboardInterrupt:
	pass

