#!/envs/laundry/bin/python

from sql_operator import *
import serial
import subprocess

def arduino_port(finder):
	# Find the port for the RFID
	arduino = os.path.expanduser(finder)
	usb = subprocess.check_output([arduino], shell = True)
	print "This is the port for the RFID antenna:", usb[:-1]
	return serial.Serial(usb[:-1], 115200, timeout = 0.1, bytesize=serial.EIGHTBITS) 

#~ ser = arduino_port("~/raspy/find_arduino.sh")

ser = serial.Serial("/dev/cu.usbmodemfa1311", 115200, timeout = 0.1, bytesize=serial.EIGHTBITS) 

def check_for_swipe( look_for = "UID Value:"):

		# Use look_for to parse out the ID you wnt to lookup/check
		line = ser.readline()
		if line is not None:
			
			print "length of line =", len(line)
			print line
			
			# A length of 6 means you're getting all 4 bytes of the UID and the
			# 	newline and return characters in the line.
			if len(line) == 6:
					
				card_id = line[:-2].encode('hex')
				print int(card_id,16)
				# print card_id
				who_swiped = decode_card(card_id)
				user = Tenant(who_swiped)
				
				
				if self.q != 0:
					new_bal = user.balance + self.q 
					self.q = 0
					user.update_balance(new_bal)
					print "New queue value:", self.q

				else:
					print "Current Balance for", user.name +":", user.balance



if __name__ == "__main__":
	while True:
		check_for_swipe()
		print "Done."
