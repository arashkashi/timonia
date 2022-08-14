from abc import abstractmethod

class Sampler:
	@abstractmethod
	def next_sample(self):
		pass
