#!/envs/laundry/bin/python

import os
import sys, time
from datetime import datetime
from daemon import Daemon
import subprocess
import eSSP
import time
from multiprocessing import Process

import serial
from sql_operator import *
from tabulate import tabulate
from threading import Thread


# MOVE THIS TO THE __init__ file...
# Figure out which /dev to listen to. 
# If it's a Mac, you're going to have to assign it manually, or change the 
# script accordingly. 
def bv_port(looker):
	# Find the port for the BV
	find_bv = os.path.expanduser(looker)
	bv = subprocess.check_output([find_bv])
	print "\nThis is the port for the Bill Validator:", bv[:-1]
	return eSSP.eSSP(bv[:-1])

def arduino_port(finder):
	# Find the port for the RFID
	arduino = os.path.expanduser(finder)
	usb = subprocess.check_output([arduino])
	print "This is the port for the RFID antenna:", usb[:-1]
	return serial.Serial(usb[:-1], 115200, timeout = 0.1, bytesize=serial.EIGHTBITS) 


if sys.platform.startswith('darwin'):
	mpath = os.path.expanduser('~/raspy/find_bv.sh')
	k = bv_port(mpath)
	mpath = os.path.expanduser('~/raspy/find_arduino.sh')
	ser = arduino_port(mpath) 
	
	# Find the port for the BV
	find_bv = os.path.expanduser('~/raspy/find_bv.sh')
	bv = subprocess.check_output([find_bv])
	print "\nThis is the port for the Bill Validator:", bv[:-1]
	k = eSSP.eSSP(bv[:-1])
	

elif sys.platform.startswith('linux'):

	# Find the port for the BV
	k = bv_port("~/laundry_prog/find_bv.sh")

	# Find the port for the RFID
	station_arduino = arduino_port("~/laundry_prog/find_arduino.sh") 
	
	# Set screen width in characters
	SCREEN_WIDTH = 16

	# Initialize serial connection
	disp = serial.Serial(port='/dev/ttyAMA0', baudrate=19200)

	




# Do some inital set-up on the usb devices.
# Start with the Bill Validator:
print k.sync()
print k.enable_higher_protocol()
# Original
print k.set_inhibits(k.easy_inhibit([1, 1, 1, 1]), '0x00')
# print k.set_inhibits(k.easy_inhibit([0, 1, 1, 1]), '0x00')
print k.enable()
bills = [1,5,10,20]




def scrolltext(text):

    # Move cursor to far right of screen, in preparation for scrolling
    cursor_start = 143

    # Initialize window's head and tail
    head = tail = 0

    while tail <= len(text):

        # Actually move the cursor to the far right as set above
        disp.write(chr(cursor_start))

        # Write out text "window"
        disp.write(text[head:tail])

        # Move the start cursor depending on whether or not the text
        # has reached the far left of the screen, as it scrolls to the left
        cursor_start = cursor_start - 1 if not cursor_start <= 128 else 128

        # Updated window  tail
        tail += 1

        # Update window head
        head = head + 1 if tail >= SCREEN_WIDTH else 0
        time.sleep(0.4)
        

def disp_bal(balance = "No record" , name = "None"):
	# Make a sound so we know the swipe worked. 
	disp.write(chr(22))
	disp.write(chr(17))
	disp.write(chr(216))
	disp.write(chr(209))
	disp.write(chr(223))
	disp.write(chr(225))
	disp.write(chr(227))
	
	# Clear the screen. 
	disp.write(chr(12))
	time.sleep(.01)
	disp.write(chr(128))
	
	# write some words
	disp.write(str(name))
	
	# Move down a line
	disp.write(chr(148))
	
	# Print the balance and wait
	disp.write("    $" + str(balance))
	time.sleep(5)
	
	# Clear the screen. 
	disp.write(chr(12))
	time.sleep(.01)
	
	disp.write(chr(21))
	disp.write(chr(18))
	
	print "The screen should now be off"


		

class Bank(object):
	"""docstring for Bank"""
	def __init__(self):
		super(Bank, self).__init__()
		print "This is a Bank object. The initial value is 0."
		# Hopefully it foesn't matter that user hasn't been initiated yet...
		self.screener = []
		self.screener.append( Process(target = disp_bal, args = (  "42","Initial Screen", )) )
		self.screener[0].start()
		self.q = 0 # This value will change
		self.account_num = int()
		self.value = 0 # This is how much TOTAL money has been collected
		self.last_swipe = None
		
		
						


	def check_for_bill(self):

		poll =  k.poll()
		# len	 pol = 0 when nothing is happening. 
		if len(poll) > 1:
	
			if len( poll[1] ) == 2 :
				if poll[1][0] == '0xee':
					rn = datetime.now()
					print "Accepted $%s on %s-%s-%s at %s:%s" % ( str(bills[poll[1][1] - 1 ]), rn.month, rn.day, rn.year, rn.hour, rn.minute )
					self.value += bills[poll[1][1] - 1 ]
					self.q += bills[poll[1][1] - 1 ]
					print "The amount in the queue is", self.q


	def check_for_swipe(self):

		# Use look_for to parse out the ID you wnt to lookup/check
		line = station_arduino.readline()
		if line is not None:
			
			#~ print "length of line =", len(line)
			#~ print line
			
			# A length of 6 means you're getting all 4 bytes of the UID and the
			# 	newline and return characters in the line.
			
			if len(line) == 6 and not self.screener[0].is_alive():
				print "this is working!"
				
				# Get the UID	
				card_id = line[:-2].encode('hex')
				
				self.last_swipe = card_id
				
				# Look up who swiped using the UID
				who_swiped = decode_card(card_id) # HEX --> INT
				
				
				return who_swiped
				
		else:
			return False
				
				
				
			
				

	# This doesn't have to be a part of the Class,
	# it can be a separate function but then it will need to be Threaded...
	def run(self):
		
		
		
		
		while True:
			#~ if len(self.screener) == 1:
				
				#~ print self.screener[0].is_alive()
			#~ else: 
				#~ "Something is different with screener, ", len(self.screener)


			self.check_for_bill()


			station_swipe = self.check_for_swipe()
			
			if station_swipe:
				print "There was a swipe at the station."
				user = Tenant(station_swipe)
				#~ self.display_on = Thread(target = disp_bal, args = (name = user.name, balance = user.balance) )	
				# If there's money saved in the queue, add it to the db then display the information. 
				if self.q != 0:
					
					new_bal = user.balance + self.q 
					
					
					
					user.update_balance(new_bal)
					self.q = 0
					print "	Queue reset to:" , self.q
					
					time.sleep(.1)
					if not self.screener[0].is_alive():
						print "The display should be started now"
						self.screener[0] = Process(target = disp_bal, args = ( int(new_bal), user.name, ) )
						self.screener[0].start()
					else:
						print "Display is on"
				
				else:
					if not self.screener[0].is_alive():
						print "The display should be started now"
						self.screener[0] = Process(target = disp_bal, args = ( int(user.balance), user.name, ) )
						self.screener[0].start()
					else:
						print "Display is on"
						
				

						
						
				#~ else:
					#~ print "Current Balance for", user.name +":", user.balance
					#~ if not self.display_on.is_alive():
						#~ self.display_on.start()
			


		



		


if __name__ == '__main__':
	
	bank = Bank()
	bank.run()

