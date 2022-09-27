import unittest
from src.sampler.sampler_csv import CSVSampler

class TestCSVSampler(unittest.TestCase):
    def test_csv_sampler(self):
        # each sample contains the following keys:
        # timestamp,prices,total_volume,market_caps,Vol_Mcap_ratio,Open,High,
        # Low,Close,Volume,Close Time,Date,moving_avg_Vol_MCap,Un_Norm_Vol_MCap,
        # Heiken_color,Greater,Slope,Pivot
        sampler = CSVSampler("./tests/test_sampler_csv/binancecoin_USDT.csv")
        totalSampleCount = 0
        while sample := sampler.next_sample():
            # check if first sample has the right price
            if totalSampleCount == 0:
                self.assertEqual(sample[1]['prices'], 37.39459108952269) 
            totalSampleCount = totalSampleCount + 1

        self.assertEqual(totalSampleCount, 604)

if __name__ == '__main__':
    unittest.main()