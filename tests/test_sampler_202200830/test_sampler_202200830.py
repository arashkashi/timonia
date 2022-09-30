import unittest
import json
from src.sampler.sampler_csv import CSVSampler
from src.sampler.sampler_20220830 import Sampler20220830
# from src.utilities import pre_processor

class TestSampler20220830(unittest.TestCase):
    def test_20220830_sampler(self):
        pass
        # sampler = Sampler20220830("melon", "usd")
        # next_sample = sampler.next_sample()

        # print(next_sample)
        # self.assertFalse(df.empty)


if __name__ == '__main__':
    unittest.main()