#!/envs/bills/bin/python

from __init__ import __sql__
import mysql.connector
import os
from tabulate import tabulate
from errors import *

# Connect to SQL Database
db = mysql.connector.connect(**__sql__)
cursor = db.cursor()

def add_row(tablename, rowdict):
	# This function adds a dictionary row to the specified table 
	
	# print "This function will add the dictionary provided to the table specified."
	# print 'add_row( tablename, rowdict )'
	# print 'tablename: ', tablename
	# print 'rowdict: ', rowdict

	# filter out keys that are not column names
	# you have to add new columns in the sqladmin page
	cursor.execute("describe %s" % tablename)
	allowed_keys = set(row[0] for row in cursor.fetchall())
	keys = allowed_keys.intersection(rowdict)

	if len(rowdict) > len(keys):
		unknown_keys = set(rowdict) - allowed_keys
		# print "\n\nskipping keys:", ", ".join(unknown_keys)

	# Make the sql string to pass to .execute()
	columns = "`" + "`,`".join(keys) + "`"
	values_template = ", ".join(["%s"] * len(keys))
	values = tuple(rowdict[key] for key in keys)

	sql = 'insert into %s (%s) values %s' % (
		tablename, columns, values)

	os.system('clear')
	cursor.execute(sql)
	db.commit()




def account_lookup(to_get, how = 'id'):
	# return basic account information
	# takes id OR name as input
	#~ print "\nLooking up account using", how + ":", to_get, "\n"
	try:
		if how == 'id':
			sql = "SELECT * FROM tenants WHERE id = %s" % (to_get)
			cursor.execute(sql)
			response = cursor.fetchall() 
			if len(response) > 1:
				raise "There were multiple responses to the query."
			return response[0]
		elif how == 'name ':
			sql = 'SELECT * FROM tenants WHERE name = "%s" '% (to_get)
			cursor.execute(sql)
			response = cursor.fetchall() 
			return response[0]
	except IndexError:
		raise CardNotFound(to_get)
	
	
		

def decode_card(babble = "0xE1 0x83 0x53 0x23"):
	id_num = babble.split(" ")
	decoded = ""
	for x in id_num:
		decoded += str(int(x,16))
	# print "decoded", decoded
	return decoded
	
	



class Database(object):
	"""docstring for Database"""
	def __init__(self, swiped):
		cursor.execute("SHOW COLUMNS IN tenants")
		self.columns = [x[0] for x in cursor.fetchall()]
		# THIS IS WHERE TO DECODE THE ID ON THE CARD! 
		self.swiped = decode_card(swiped)
		# self.swiped = swiped
		


	def all_tenants(self):
		# Contents of 
		sql = "select * from tenants"
		cursor.execute(sql)
		alls = cursor.fetchall()
		print tabulate( alls,  headers = self.columns)
		return alls

	all_tenants = property(all_tenants)

	def add_tenant(self, tenant_dict, active = 1):
		# Make the default setting active == 1
		tenant_dict['active'] = active
		add_row("tenants", tenant_dict)

	def credit_account(self, dollars_inserted):
		# Looks up what was in the db before they swiped the card. 
		# 	Adds the dollar amount they had to what they just inserted. 
		#	Updates the database.
		card_number = self.swiped
		previous_balance = account_lookup(card_number)[3]
		new_balance = previous_balance + dollars_inserted
		upper = 'UPDATE tenants set balance = %s where id = %s' % (new_balance, card_number[0])
		cursor.execute(upper)
		db.commit()

	
	def tenant_info(self):
		just_one = account_lookup(self.swiped[0])
		print tabulate( [just_one],  headers = self.columns)
		print "\n\n"
		return just_one
		
	def debit_account(self, debit_amount):
		# Decreases the value of balance in database. 
		# 	To be used when a machine is started. 
		card_number = self.swiped[0]
		previous_balance = account_lookup(card_number)[3]
		new_balance = previous_balance - debit_amount
		finalize = 'UPDATE tenants set balance = %s where id = %s' % (new_balance, card_number)
		cursor.execute(finalize)
		db.commit()
		
	
class Tenant(object):
	"""docstring for Tenant"""
	def __init__(self, data ):
		#~ data = account_lookup(card_ID)
		self.data = data
		self.id = data[0]
		self.apartment = data[1]
		self.name = data[2]
		self.balance = data[3]
		self.last_transaction = data[4]


	def update_balance(self, new_balance):
		# Looks up what was in the db before they swiped the card. 
		# 	Adds the dollar amount they had to what they just inserted. 
		#	Updates the database.
		
		
		upper = 'UPDATE tenants set balance = %s where id = %s' % (new_balance, self.id)
		cursor.execute(upper)
		db.commit()
		print "--> Balance for", self.name, "updated successfully! "
		print "--> New Balance:", new_balance

	def function():
		pass

	



demo_tenant = {
	"name" : "Paddy Lauber",
	"id" : '4567',
	"apartment" : 4,
}

if __name__ == '__main__':
	# database = Database('MjM0NTYsMixSb2JieSBTaGludGFuaSwzMC4wLDIwMTUtMDctMjQgMjM6MDc6NDksMCw=')
	# database.all_tenants
	# database.add_tenant(demo_tenant, 1)
	# database.credit_account(15)
	# database.tenant_info()
	
	# done = ""
	# for x in database.tenant_info('Robby Shintani'):
	# 	done += str(x) + ","
	# print "done:",done
	# database.debit_account(10)
	# database.all_tenants
	print decode_card()

