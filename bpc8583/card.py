class Card:
	def __init__(self, pan=None, expiry_date=None, service_code=None):
		if pan:
			self.pan = pan
		else:
			self.pan = '8990019898989989'

		if expiry_date:
			self.expiry_date = expiry_date
		else:
			self.expiry_date = '1809'

		if service_code:
			self.service_code = service_code
		else:
			self.service_code = '101'

		self.track2_data = '1872300000720'

	def get_card_number(self):
		return int(self.pan)

	def get_track2(self):
		return self.pan + '=' + self.expiry_date + self.service_code + self.track2_data
