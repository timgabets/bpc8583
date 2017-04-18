class Card:
	def __init__(self, pan=None, expiry_date=None, service_code=None, pvvki=None, PVV=None, CVV=None, discretionary_data1=None, discretionary_data2=None):
		"""
		"""
		if pan:
			self.pan = str(pan)
		else:
			self.pan = '8990011234567890'

		if expiry_date:
			self.expiry_date = str(expiry_date)
		else:
			self.expiry_date = '1809'

		if service_code:
			self.service_code = str(service_code)
		else:
			self.service_code = '101'

		if pvvki:
			self.PVV_key_index = str(pvvki)
		else:
			self.PVV_key_index = '1'

		if PVV:
			self.PVV = str(PVV)
		else:
			self.PVV = '8723'

		if CVV:
			self.CVV = str(CVV)
		else:
			self.CVV = '000'

		if discretionary_data1:
			self.discretionary_data1 = str(discretionary_data1)
		else:
			self.discretionary_data1 = '00'

		if discretionary_data2:
			self.discretionary_data2 = str(discretionary_data2)
		else:
			self.discretionary_data2 = '720'

		print('Card {} created'.format(self.pan)) 


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
		return self.pan + '=' + self.expiry_date + self.service_code + self.PVV_key_index + self.PVV + self.CVV + self.discretionary_data1 + self.discretionary_data2


	def get_sequence_number(self):
		"""
		"""
		return 1
