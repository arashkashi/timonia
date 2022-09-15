from abc import abstractmethod
import math
import logging

class Trader:
	def __init__(self, initial_funds):
		# Assets is a map {"name_id": number_of_coins}
		self.assets = {}
		self.funds = initial_funds

	def buy(self, name_id, price):
		# How many I could buy?
		numbers_can_buy = math.floor(self.funds/price)

		if numbers_can_buy < 1: 
			return False

		# Deduct from funds.
		self.funds = self.funds - numbers_can_buy * price

		# Update assets
		current_amount = self.assets.get(name_id, 0)
		self.assets[name_id] = current_amount + numbers_can_buy

		return True

	def sell(self, name_id, price):
		current_amount = self.assets.get(name_id, 0)
		if current_amount == 0:
			return False

		self.assets[name_id] = 0
		self.funds = self.funds + price * current_amount
		return True

