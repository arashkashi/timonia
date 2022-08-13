import argparse
from messages.messages import HelloWorld

parser = argparse.ArgumentParser()
parser.add_argument("--inputfile",
                    help="input filename for simulation")
args = parser.parse_args()

if args.inputfile:
	print(args.inputfile)
else:
	print("Error: please use help option")

hello_world_string = "Hello World"
hello_world_object = HelloWorld(hello_world_string)
hello_world_object.hello_world_method()
