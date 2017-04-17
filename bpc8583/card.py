class Card:
	def __init__(self, pan=None, expiry_date=None, service_code=None, discretionary_data=None):
		"""
		"""
		if pan:
			self.pan = pan
		else:
			self.pan = '8990011234567890'

		if expiry_date:
			self.expiry_date = expiry_date
		else:
			self.expiry_date = '1809'

		if service_code:
			self.service_code = service_code
		else:
			self.service_code = '101'

		if discretionary_data:
			self.discretionary_data = discretionary_data
		else:
			self.discretionary_data = '1872300000720'


	def get_card_number(self):
		"""
		"""
		return int(self.pan)


	def get_expiry_date(self):
		"""
		"""
		return int(self.expiry_date)


	def get_track2(self):
		"""
		"""
		return self.pan + '=' + self.expiry_date + self.service_code + self.discretionary_data


	def get_sequence_number(self):
		"""
		"""
		return 1
