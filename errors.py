
# This is an ERROR CLASS
class CardNotFound(Exception):
	def __init__(self, card_id):
		self.card_id = card_id
	
	
	
if __name__ == "__main__":
	try:
		raise CardNotFound(12343)
	except CardNotFound as aa:
		print "This is within a try/except statement."
		print "	", aa.card_id
	print "Something goes here"
		
	
