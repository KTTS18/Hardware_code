import serial
import time
import string
import pynmea2
import datetime
import pymongo

MONGO_DETAILS = 'mongodb+srv://TANdb:Tan180704@cluster0.vw9z5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = pymongo.MongoClient(MONGO_DETAILS)
db = client.myFirstDatabase

try :
	while True:
		port = "/dev/ttyAMA0"
		ser = serial.Serial(port, baudrate=9600, timeout=0.5)
		dataout = pynmea2.NMEAStreamReader()
		newdata = ser.readline()

		if newdata[0:6] == "$GPRMC":
			newmsg = pynmea2.parse(newdata)
			lat = newmsg.latitude
			lng = newmsg.longitude
			gps = "Lat = ",float(lat),"and Long = ",float(lng)
			print(gps)
			now = datetime.datetime.now()
               	 	print(now.strftime("Day: %d/%m/%y Time: %H:%M:%S"))
			data = {
    				"lat":  float(lat),
   					"long": float(lng),
    				"date": now.strftime("Day: %d/%m/%y Time: %H:%M:%S"),
    				"blind": "61515017"
					}
			db.location.insert(data)
			time.sleep(29)
except KeyboardInterrupt : 
	print("Force quit..")