#!/usr/bin/python

# To install evdev on the pi..
# 	$ apt-get install python-dev python-pip gcc
# 	$ apt-get install linux-headers-$(uname -r)

# This is the main script for the laundry room program. 

# Start the bill acceptor daemon.

# Start RFID daemon. 

# Start washer daemon. 

# Start dryer daemon.

# On card swipe at STATION:
# 	Decode stored information. 
# 	Verify it matches what we have. 
# 	If it does, 
# 		Add the value
# 	Else
# 		Don't add the value?

# On card sipe at washer[i]:
# 	

import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
	print ser.readline()
