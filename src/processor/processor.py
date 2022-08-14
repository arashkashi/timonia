from abc import abstractmethod

class Processor:
	@abstractmethod
	def on_next_sample(self, next_sample):
		pass
