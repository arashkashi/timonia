from src.sampler.sampler import Sampler
import pandas as pd

# This sampler simply reads from aa CSV file with the mentioned coloumns
# imestamp, prices,	total_volume, market_caps,
# Vol_Mcap_ratio, Open,	High,	Low	Close,	Volume,	Close Time,
# Date,	moving_avg_Vol_MCap,	Un_Norm_Vol_MCap,	Heiken_color, 
# Greater, Slope, Pivot
class CSVSampler(Sampler):
	def __init__(self, filename):
		self.df = pd.read_csv(filename)
		self.dfIterator = self.df.iterrows()

	def __del__(self):
		pass

	def next_sample(self):
		try:
			return next(self.dfIterator)
		except StopIteration:
			return None



