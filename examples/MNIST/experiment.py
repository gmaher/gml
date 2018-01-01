import os

import io_
from interface import AbstractExperiment

class MNISTExperiment(AbstractExperiment):
    def __init__(self,config):
        self.config = config
        self.DATA_DIR = config['DATA_DIR']

    def load(self,config):
        raise RuntimeError("abstract not implemented")
    def predict(self):
        raise RuntimeError("abstract not implemented")
    def train(self):
        raise RuntimeError("abstract not implemented")
    def evaluate(self):
        raise RuntimeError("abstract not implemented")

    ####################
    # Extra Functions
    ####################
    def load_example(self,id):
        meta = io.load_yaml(self.DATA_DIR+'/{}.meta.yaml'.format(id))
        x = np.load(meta['x'])
        y = meta['y']

        if self.config['NORMALIZE'] == 'MEAN':
            x = (1.0*x-meta['MEAN'])/meta['STD']

        if self.config['NORMALIZE'] == 'MAX':
            x = (1.0*x-np.amin(x))/(np.amax(x)-np.amin(x))

        x = x.reshape([1]+x.shape)

        return (x,y)

    def get_yamls(self):
        l = os.listdir(self.DATA_DIR)
        l = [f for f in l if '.yaml' in f]
        l = [io_.load_yaml(f) for f in l]
        return l
