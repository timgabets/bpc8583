from bpc8583.tools import get_random_hex

class Card:
	def __init__(self, pan=None, expiry_date=None, service_code=None, pvvki=None, PVV=None, CVV=None, discretionary_data=None, description=None):
		"""
		"""
		self.trxn_counter = 0
		self.set_description(description)

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
			self.service_code = '201'

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

		if discretionary_data:
			self.discretionary_data = str(discretionary_data)
		else:
			self.discretionary_data = ''

	def get_iss_application_data(self):
		"""
		Get ICC Issuer Application data (Contains proprietary application data for transmission to the issuer in an online transaction)
		"""
		return '0000'


	def get_application_cryptogram(self):
		"""
		Return ICC application crytpogram (returned by the ICC in response of the GENERATE AC command)
		"""
		self.trxn_counter += 1
		return get_random_hex(16)


	def _set_transaction_counter(self, counter):
		"""
		"""
		self.trxn_counter = counter


	def get_transaction_counter(self):
		"""
		Get ICC application transaction counter
		"""
		return str(self.trxn_counter).rjust(4, '0')


	def get_card_number(self):
		"""
		"""
		return self.get_int_card_number()


	def get_service_code(self):
		"""
		"""
		return self.service_code


	def get_int_card_number(self):
		"""
		"""
		return int(self.pan)


	def get_str_card_number(self):
		"""
		"""
		return self.pan


	def get_expiry_date(self):
		"""
		"""
		return int(self.expiry_date)


	def get_track2(self):
		"""
		"""
		return self.pan + '=' + self.expiry_date + self.service_code + self.PVV_key_index + self.PVV + self.CVV + self.discretionary_data


	def get_sequence_number(self):
		"""
		"""
		return 1

	def set_description(self, description):
		"""
		"""
		if description: 
			self.description = description
		else:
			self.description = ''


	def get_description(self):
		"""
		"""
		return self.description

