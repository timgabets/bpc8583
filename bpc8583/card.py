class Card:
	def __init__(self, pan):
		self.pan = pan
		self.track2_data = '18091011872300000720'

	def get_card_number(self):
		return self.pan

	def get_track2(self):
		return self.pan + '=' + self.track2_data
