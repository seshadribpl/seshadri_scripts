# Demonstration of classmethod
# Examples on how to call the methods in the class or instantiate it:
'''
Katiroll.paneer()
Katiroll.chana()
newItem = Katiroll('corn', 22)
Katiroll(['salt', 'pepper', 'chillies'], 25)
'''



class Katiroll:
	def __init__(self,ingredients,price):
		self.ingredients = ingredients
		self.price = price
		print 'from the class itself'
		print self.ingredients 
		print self.price
		print '---------------------'

	@classmethod
	def chana(cls):
		return cls(['kabuli chana', 'onions'], 20)

	@classmethod
	def paneer(cls):
		return cls(['paneer', 'potatoes', 'chaat masala'], 25)
		paneer_roll = cls(['paneer', 'potatoes', 'chaat masala'])
		print 'from the classmethod'
		print paneer_roll
		print '---------------------'




