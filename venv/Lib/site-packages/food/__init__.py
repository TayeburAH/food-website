import random

class Food():
	def eat(self):
		if self.exists:
			if self.deliciousness >= 100:
				print(self.good.format(self.deliciousness))
			else:
				print(self.bad)
			self.exists = False
			self.deliciousness = 0
		else:
			print(self.already_eaten)
	def __repr__(self):
		if self.exists:
			return self.string
		else:
			return 'None'
	def __str__(self):
		if self.exists:
			return self.string
		else:
			return 'None'

class Cookie(Food):
	def __init__(self):
		self.deliciousness = random.randint(50,1000)
		self.exists = True
		self.good = 'yum, deliciousness level is {}'
		self.bad = 'eww moldy cookie'
		self.already_eaten = 'cookie has already been eaten'
		self.string = ' 🍪 '


class Taco(Food):
	def __init__(self):
		self.deliciousness = random.randint(50,500)
		self.exists = True
		self.good = 'yum, deliciousness level is {}'
		self.bad = 'eww disgusting taco'
		self.already_eaten = 'taco has already been eaten'
		self.string = ' 🌮 '
