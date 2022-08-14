import unittest
from src.sampler.simulation_sampler import SimulationSampler

class TestReadData(unittest.TestCase):
    def test_upper(self):
        sampler = SimulationSampler("./tests/data/hellow_world_test_data.txt")
        counter = 0
        while sample := sampler.next_sample():
            if counter == 0:
                self.assertEqual(sample, "259.5900")
            if counter == 755:
                self.assertEqual(sample, "221.3100")
            counter = counter + 1
        self.assertEqual(counter, 756)

if __name__ == '__main__':
    unittest.main()