import unittest
from src.sampler.sampler_csv import CSVSampler
from src.processor.simulation_processor_babak import SimulationProcessorBabak
from src.trader.trader import Trader
import logging
import matplotlib.pyplot as plt

class TestCSVSampler(unittest.TestCase):
    def test_lag_20220830(self):
        logging.basicConfig(filename='./logs/test_algo_20220830.log', level=logging.DEBUG)
        # each sample contains the following keys:
        # timestamp,prices,total_volume,market_caps,Vol_Mcap_ratio,Open,High,
        # Low,Close,Volume,Close Time,Date,moving_avg_Vol_MCap,Un_Norm_Vol_MCap,
        # Heiken_color,Greater,Slope,Pivot
        sampler = CSVSampler("./tests/test_sampler_csv/binancecoin_USDT.csv")
        trader = Trader(1000)
        processor = SimulationProcessorBabak(trader)
        totalSampleCount = 0
        last_price = 0.0
        while sample := sampler.next_sample():
            last_price = sample[1]['prices']
            processor.on_next_sample(sample[1])

        trader.sell("binancecoin", last_price)
        logging.info(f'Concluded alg-20220830 with funds {trader.funds}')

        self.assertEqual(len(processor.buys), len(processor.samples))

        # Uncomment to see the plot results.
        # plt.plot(list(map(lambda x: x['prices'], processor.samples)))
        # plt.plot(list(map(lambda x: x[0]['prices'] if x[1] == 1 else 0, zip(processor.samples, processor.buys))), 'r+')
        # plt.plot(list(map(lambda x: x[0]['prices'] if x[1] == 1 else 0, zip(processor.samples, processor.sells))), 'bo')
        # plt.show()
        # plt.plot(list(map(lambda x: x['prices'], processor.samples)))
        # plt.plot(list(map(lambda x: x[0]['prices'] if x[1] == 1 else 0, zip(processor.samples, processor.buys))), 'r+')
        # plt.plot(list(map(lambda x: x[0]['prices'] if x[1] == 1 else 0, zip(processor.samples, processor.sells))), 'bo')
        # plt.show()



if __name__ == '__main__':
    unittest.main()