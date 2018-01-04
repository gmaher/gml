import yaml
import csv
import os

def load_yaml(fn):
    """loads a yaml file into a dict"""
    with open(fn,'r') as file_:
        try:
            return yaml.load(file_)
        except RuntimeError as e:
            print "failed to load yaml fille {}, {}\n".format(fn,e)

def save_yaml(fn, data):
    with open(fn,'w') as file_:
        yaml.dump(data,file_, default_flow_style=False)

def parse_config(config_filename):
    config_file = os.path.abspath(config_filename)
    if '.yaml' not in config_file:
        raise RuntimeError('config file must be a yaml file')

    config = load_yaml(config_file)

    if not config.has_key('EXPERIMENT_FILE'):
        raise RuntimeError('config file must specify EXPERIMENT_FILE')

    if not config.has_key('EXPERIMENT_NAME'):
        raise RuntimeError('config file must specify EXPERIMENT_NAME')

    return config
