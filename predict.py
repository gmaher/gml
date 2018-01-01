import importlib
import argparse
import os

import io_

parser = argparse.ArgumentParser()
parser.add_argument('config_file')
parser.add_argument('--val', action='store_true')
parser.add_argument('--test', action='store_true')
parser.add_argument('--evaluate', action='store_true')

args = parser.parse_args()

config_file = os.path.abspath(args.config_file)

do_val      = args.val
do_test     = args.test
do_evaluate = args.evaluate

config = io_.get_config(args.config_file)

Experiment = importlib.import_module(config['EXPERIMENT_NAME'],
    config['EXPERIMENT_FILE'])

experiment = Experiment(config)

experiment.load(config)

if do_val:
    val_list = experiment.get_train_list()

    experiment.predict(val_list)

    if do_evaluate: experiment.evaluate(val_list)

if do_test:
    test_list = experiment.get_test_list()

    experiment.predict(test_list)

    if do_evaluate: experiment.evaluate(test_list)
