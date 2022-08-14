import argparse

from src.sampler.simulation_sampler import SimulationSampler
from src.processor.simulation_processor import SimulationProcessor

parser = argparse.ArgumentParser()
parser.add_argument("--inputfile",
                    help="input filename for simulation")
args = parser.parse_args()

if args.inputfile:
	sampler = SimulationSampler(args.inputfile)
	processor = SimulationProcessor()
	while next_sample := sampler.next_sample():
		processor.on_next_sample(next_sample)

else:
	print("Error: please use help option")

