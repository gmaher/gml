import numpy as np
import tensorflow as tf
import os
import sys
sys.path.append(os.path.abspath('../../'))
import io_
from tqdm import tqdm

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('config_file')
args = parser.parse_args()
config_file = os.path.abspath(args.config_file)
config = io_.load_yaml(config_file)

dataset = tf.contrib.learn.datasets.load_dataset('mnist')

X = dataset.train.images
Y = dataset.train.labels

DATA_DIR = os.path.abspath(config['DATA_DIR'])

f = open('id_list.txt','w')
for i in tqdm(range(1000)):

    set_ = ""
    r = np.random.rand()
    if r <= 0.5: set_ = 'TRAIN'
    if r > 0.5 and r <= 0.75: set_ = 'VAL'
    if r > 0.75: set_ = "TEST"
    meta = {}
    meta['id'] = i
    meta['x'] = DATA_DIR+'/{}.x.npy'.format(i)
    meta['y'] = int(Y[i])
    meta['SET'] = set_
    meta['MEAN'] = float(np.mean(X[i]))
    meta['STD'] = float(np.std(X[i]))
    io_.save_yaml(DATA_DIR+'/{}.meta.yaml'.format(i),meta)
    np.save(DATA_DIR+'/{}.x.npy'.format(i),X[i])
