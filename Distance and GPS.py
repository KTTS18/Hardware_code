import RPi.GPIO as GPIO
import serial
import time
import string
import pynmea2
import datetime
import pymongo
import multiprocessing
GPIO.setmode(GPIO.BCM)

MONGO_DETAILS = 'mongodb+srv://TANdb:Tan180704@cluster0.vw9z5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = pymongo.MongoClient(MONGO_DETAILS)
db = client.myFirstDatabase
GPIO.setmode(GPIO.BCM)

GPIO_BUZZER1 = 5
GPIO_TRIGGER1 = 9
GPIO_ECHO1 = 11

GPIO_BUZZER2 = 6
GPIO_TRIGGER2 = 27
GPIO_ECHO2 = 22

GPIO.setup(GPIO_BUZZER1, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)

GPIO.setup(GPIO_BUZZER2, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)

def distance():
  GPIO.output(GPIO_TRIGGER1, True) # set TRIGGER to HIGH
  time.sleep(0.5) # wait 10 microseconds
  GPIO.output(GPIO_TRIGGER1, False) # set TRIGGER back to LOW
  start = time.time()
  stop = time.time()

  while (GPIO.input(GPIO_ECHO1) == 0):
    start = time.time()
    #print("loop3")
    if ((start-stop) >= 5):
      break

  while (GPIO.input(GPIO_ECHO1) == 1):
    stop = time.time()
    #print("loop4")
    if ((start-stop) >= 5):
      break

  measuredTime = stop - start
  distanceBothWays = measuredTime * 33112 # cm/s in 20 degrees Celsius
  distance = distanceBothWays / 2
  print("Distance1 : {0:5.1f}cm".format(distance))
  
  return distance

def distance2():
  GPIO.output(GPIO_TRIGGER2, True) # set TRIGGER to HIGH
  time.sleep(0.5) # wait 10 microseconds
  GPIO.output(GPIO_TRIGGER2, False) # set TRIGGER back to LOW
  start = time.time()
  stop = time.time()

  while (GPIO.input(GPIO_ECHO2) == 0):
    start = time.time()
    #print("loop1")
    if ((start-stop) >= 5):
      break

  while (GPIO.input(GPIO_ECHO2) == 1):
    stop = time.time()
    #print("loop2")
    if ((start-stop) >= 5):
      break

  measuredTime = stop - start
  distanceBothWays = measuredTime * 33112 # cm/s in 20 degrees Celsius
  distance = distanceBothWays / 2
  print("Distance2 : {0:5.1f}cm".format(distance))
  
  return distance

def beep_freq():
    dist = distance()
    if (dist > 80):
        return -1
    elif (dist <= 80 and dist >=70):
        return 1
    elif (dist < 60 and dist >= 50):
        return 0.5
    elif (dist < 50 and dist >= 30):
        return 0.25
    else:
        return 0

def beep_freq2():
    dist2 = distance2()  
    if (dist2 > 70):
        return -1
    elif (dist2 <= 70 and dist2 >=60):
        return 1
    elif (dist2 < 60 and dist2 >= 50):
        return 0.5
    elif (dist2 < 50 and dist2 >= 40):
        return 0.25
    else:
        return 0

def rundistance():
  try:
    while True:
        freq = beep_freq()
        freq2 = beep_freq2()
        if freq == -1:
            GPIO.output(GPIO_BUZZER1, False)
            time.sleep(0.25)
        elif freq == 0:
            GPIO.output(GPIO_BUZZER1, True)
            time.sleep(0.25)
        else:
            GPIO.output(GPIO_BUZZER1, True)
            time.sleep(0.1) # Beep is 0.1 seconds long
            GPIO.output(GPIO_BUZZER1, False)
            time.sleep(freq)
        
        if freq2 == -1:
            GPIO.output(GPIO_BUZZER2, False)
            time.sleep(0.25)
        elif freq2 == 0:
            GPIO.output(GPIO_BUZZER2, True)
            time.sleep(0.25)
        else: 
            GPIO.output(GPIO_BUZZER2, True)
            time.sleep(0.1) # Beep is 0.1 seconds long
            GPIO.output(GPIO_BUZZER2, False)
            time.sleep(freq2) # Pause between beeps = beeping frequency
   
  except KeyboardInterrupt:
    GPIO.output(GPIO_BUZZER1, False)
    GPIO.output(GPIO_BUZZER2, False)
    print("Force quit..")
    GPIO.cleanup()		
    
def rungps():
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
    	       		  "blind": "60878306b0c6f846882fd2d4"
					}
			db.locations.insert(data)
			time.sleep(29)
				
if __name__ == "__main__":
   main()
   
 


