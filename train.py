import argparse

from Mindblocks.interface import BasicInterface

interface = BasicInterface()

parser = argparse.ArgumentParser(description='Train (and test) a model with a given block.')
parser.add_argument('--block')
args = parser.parse_args()

block_filepath = "blocks/test.xml" #args.block
block_name = ".".join(block_filepath.split('/')[-1].split(".")[:-1])

data_filepath = "data/toy"
interface.load_file(block_filepath)
interface.set_variable("data_folder", data_filepath)
interface.initialize()

print("====================")
pred = interface.predict()
print(pred)