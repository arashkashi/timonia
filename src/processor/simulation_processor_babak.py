class SimulationProcessorBabak:
	def __init__(self, trader):
		self.samples = []
		self.trader = trader

	def on_next_sample(self, next_sample):
		self.samples.append(next_sample)
		self.process_current_samples()
	
	def process_current_samples(self):
		# Let's make a simple algorith and if the price of this sample
		# is higher than the last two samples, indicating the market
		# raising and hence a buy signal. And an opposite for sell signal.
		if len(self.samples) < 3:
			return

		last_price = self.samples[-1]['prices']

		if (self.samples[-1]['prices'] > self.samples[-2]['prices']) and (self.samples[-2]['prices'] > self.samples[-3]['prices']):
			self.trader.buy("binancecoin", last_price)
			return

		if (self.samples[-1]['prices'] < self.samples[-2]['prices']) and (self.samples[-2]['prices'] < self.samples[-3]['prices']):
			self.trader.sell("binancecoin", last_price)
			return