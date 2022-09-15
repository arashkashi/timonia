class SimulationProcessorBabak:
	def __init__(self, trader):
		self.samples = []
		self.trader = trader

		self.buys = []
		self.sells = []

	def on_next_sample(self, next_sample):
		self.samples.append(next_sample)
		self.process_current_samples()

	def on_successfull_buy(self):
		self.buys.append(1)
		self.sells.append(0)

	def on_successfull_sell(self):
		self.buys.append(0)
		self.sells.append(1)

	def on_no_trade_signal(self):
		self.buys.append(0)
		self.sells.append(0)
	
	def process_current_samples(self):
		# Let's make a simple algorith and if the price of this sample
		# is higher than the last two samples, indicating the market
		# raising and hence a buy signal. And an opposite for sell signal.
		if len(self.samples) < 3:
			self.on_no_trade_signal()
			return

		last_price = self.samples[-1]['prices']

		success_buy = False
		success_sell = False

		if (self.samples[-1]['prices'] > self.samples[-2]['prices']) and (self.samples[-2]['prices'] > self.samples[-3]['prices']):
			success_buy = self.trader.buy("binancecoin", last_price)
		elif (self.samples[-1]['prices'] < self.samples[-2]['prices']) and (self.samples[-2]['prices'] < self.samples[-3]['prices']):
			success_sell = self.trader.sell("binancecoin", last_price)

		if success_buy:
			self.on_successfull_buy()
		elif success_sell:
			self.on_successfull_sell()
		else:
			self.on_no_trade_signal()