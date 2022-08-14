from src.sampler.sampler import Sampler

class SimulationSampler(Sampler):
	def __init__(self, filename):
		self.fp = open(filename, 'r')

	def __del__(self):
		pass
		# self.fp.close()

	def next_sample(self):
		return self.fp.readline().replace("\n", "")


