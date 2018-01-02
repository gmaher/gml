import os
import io_
from interface import AbstractExperiment

def get_experiment(config,args):
    
def load_example(id):
    meta = io.load_yaml(self.DATA_DIR+'/{}.meta.yaml'.format(id))
    x = np.load(meta['x'])
    y = meta['y']

    if self.config['NORMALIZE'] == 'MEAN':
        x = (1.0*x-meta['MEAN'])/meta['STD']

    if self.config['NORMALIZE'] == 'MAX':
        x = (1.0*x-np.amin(x))/(np.amax(x)-np.amin(x))

    x = x.reshape([1]+x.shape)

    return (x,y)

def get_yamls(data_dir):
    l = os.listdir(data_dir)
    l = [f for f in l if '.yaml' in f]
    l = [io_.load_yaml(f) for f in l]
    return l
