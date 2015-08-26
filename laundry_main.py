#!/envs/laundry/bin/python

import os
import sys, time
from datetime import datetime
from daemon import Daemon
import subprocess
import eSSP
import time
import multiprocessing as mp

import serial
from sql_operator import *
from tabulate import tabulate


# MOVE THIS TO THE __init__ file...
# Figure out which /dev to listen to. 
# If it's a Mac, you're going to have to assign it manually, or change the 
# script accordingly. 
if sys.platform.startswith('darwin'):
	k = eSSP.eSSP("/dev/cu.usbmodemfa1331")
	ser = serial.Serial("/dev/cu.usbmodemfa1341", 115200, timeout = 0.1) 

elif sys.platform.startswith('linux'):

	# Find the port for the BV
	find_bv = os.path.expanduser('~/laundry_prog/find_bv.sh')
	bv = subprocess.check_output([find_bv])
	print "\nThis is the port for the Bill Validator:", bv[:-1]
	k = eSSP.eSSP(bv[:-1])

	# Find the port for the RFID
	arduino = os.path.expanduser('~/laundry_prog/find_arduino.sh')
	usb = subprocess.check_output([arduino])
	print "This is the port for the RFID antenna:", usb[:-1]
	ser = serial.Serial(usb[:-1], 115200, timeout = 0.1) 




		
print k.sync()
print k.enable_higher_protocol()
# Original
print k.set_inhibits(k.easy_inhibit([1, 1, 1, 1]), '0x00')
# print k.set_inhibits(k.easy_inhibit([0, 1, 1, 1]), '0x00')
print k.enable()
bills = [1,5,10,20]

		

class Bank(Daemon):
	"""docstring for Bank"""
	def __init__(self, pid = '/tmp/accepting-bills420.pid'):
		super(Bank, self).__init__(pid)
		print "This is a Bank object. The initial value is 0."
		self.q = 0 # This value will change
		self.account_num = int()
		self.value = 0 # This is how much TOTAL money has been collected


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



	def run(self):
		
		while True:


			self.check_for_bill()


			self.check_for_swipe()


		



		


if __name__ == '__main__':
	daemon = Bank()
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
			sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)

