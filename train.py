import importlib
import argparse
import os

import io_

parser = argparse.ArgumentParser()
parser.add_argument('config_file')
parser.add_argument('--load', action='store_true')

args = parser.parse_args()
do_load = args.load

config = io_.get_config(args.config_file)

Experiment = importlib.import_module(config['EXPERIMENT_NAME'],
    config['EXPERIMENT_FILE'])

experiment = Experiment(config)

if do_load: experiment.load_model(config)

train_list = experiment.get_train_list()

experiment.train(train_list)
