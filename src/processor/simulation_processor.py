class SimulationProcessor:
	def __init__(self):
		self.counter = 0
		self.last_sample = None

	def on_next_sample(self, next_sample):
		price = float(next_sample)

		if last_price := self.last_sample:
			if last_price < price:
				self.counter = self.counter + 1
		if self.counter == 30:
			self.counter = 0
			print(f'BUY at: {price}')
		self.last_sample = price
