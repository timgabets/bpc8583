class Terminal:

	def __init__(self, id=None, merchant=None):
		if id:
			self.terminal_id = id
		else:
			self.terminal_id = '10001337'

		if merchant:
			self.merchant_id = merchant
		else:
			self.merchant_id = '999999999999001'

		self.currency = '643'


	def get_terminal_id(self):
		"""
		"""
		return self.terminal_id


	def get_merchant_id(self):
		"""
		"""
		return self.merchant_id

	def get_currency_code(self):
		"""
		"""
		return self.currency
