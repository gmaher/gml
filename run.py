import importlib
import argparse
import os

import io_

parser = argparse.ArgumentParser()
parser.add_argument('config_file')
parser.add_argument('run_type',default='predict',
    choices=['train','predict','evaluate'])

parser.add_argument('--args', nargs='*')

args = parser.parse_args()

config = io_.get_config(args.config_file)

experiment_factory = importlib.import_module(config['EXPERIMENT_FILE'])

experiment = experiment_factory.get_experiment(config,args)

if args.run_type == 'train':
    print "Starting experiment training"

    experiment.train()

elif args.run_type == 'predict':
    print "Starting experiment prediction"

    experiment.predict()

elif args.run_type == "evaluate":
    print "Starting experiment evaluation"

    experiment.evaluate()
