import os
import sys
sys.path.append(os.path.abspath('..'))
from gml.gml_experiments.imputation import get_app
from gml.gml_io.io import load_json

from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

base_filepath = __file__
filename = base_filepath.split('/')[-1]
base_dir = os.path.abspath(base_filepath).replace(filename,'')
base_dir = os.path.abspath(base_dir+'/..')

config_file = base_dir+'/projects/gaussian/config.json'
config = load_json(config_file)

App = get_app(base_dir, config)
App.train()
