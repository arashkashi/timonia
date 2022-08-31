import unittest
from src.sampler.csv_sampler import CSVSampler
from src.processor.simulation_processor_babak import SimulationProcessorBabak
from src.trader.trader import Trader
import logging

class TestCSVSampler(unittest.TestCase):
    def test_csv_sampler(self):
        logging.basicConfig(filename='./logs/test_algo_20220830.log', level=logging.DEBUG)
        # each sample contains the following keys:
        # timestamp,prices,total_volume,market_caps,Vol_Mcap_ratio,Open,High,
        # Low,Close,Volume,Close Time,Date,moving_avg_Vol_MCap,Un_Norm_Vol_MCap,
        # Heiken_color,Greater,Slope,Pivot
        sampler = CSVSampler("./tests/test_csv_sampler/binancecoin_USDT.csv")
        trader = Trader(1000)
        processor = SimulationProcessorBabak(trader)
        totalSampleCount = 0
        last_price = 0.0
        while sample := sampler.next_sample():
            last_price = sample[1]['prices']
            processor.on_next_sample(sample[1])

        trader.sell("binancecoin", last_price)
        logging.info(f'Concluded alg-20220830 with funds {trader.funds}')


if __name__ == '__main__':
    unittest.main()