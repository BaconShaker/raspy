
# This is an ERROR CLASS
class CardNotFound(Exception):
	def __init__(self, card_id):
		self.card_id = card_id
	
	
	
if __name__ == "__main__":
	
	raise CardNotFound(12343)
		
	
