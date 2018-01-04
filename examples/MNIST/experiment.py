import os
import sys
sys.path.append(os.path.abspath('../../'))
import io_
from interface import AbstractTrainer, AbstractPredictor, AbstractModel, AbstractExperiment

from dataset import SequentialFileDataset

def get_experiment(config,args):
    yamls      = get_yamls(config['DATA_DIR'])
    train_list = [config['DATA_DIR']+'/{}.meta.yaml'.format(y['id'])
        for y in yamls if y['SET'] == 'TRAIN']
    val_list   = [config['DATA_DIR']+'/{}.meta.yaml'.format(y['id'])
        for y in yamls if y['SET'] == 'VAL']
    test_list  = [config['DATA_DIR']+'/{}.meta.yaml'.format(y['id'])
        for y in yamls if y['SET'] == 'TEST']

    post_processor = create_postprocessor(config)

    train_dataset = SequentialFileDataset(file_list=train_list,
        reader=load_example,
        post_processor=post_processor)

    model = MNISTModel()

    trainer   = AbstractTrainer(model, train_dataset)
    predictor = AbstractPredictor(model, train_dataset, store_prediction)

    return AbstractExperiment(trainer, predictor, predictor)

######################################
# Function Definitions
######################################
class MNISTModel(AbstractModel):
    def __init__(self):
        self.a = 0
        self.c   = 0

    def predict(self,x):
        return self.a

    def train(self,x,y):
        self.a = (1.0*self.c)/(self.c+1)*self.a + 1.0/(self.c+1)*y
        self.c += 1

def store_prediction(self,T,P):
    print "predicted label {}, actual label {}".format(P,T[1])

def load_example(meta_file):
    meta = io.load_yaml(meta_file)
    x = np.load(meta['x'])
    y = meta['y']

    return (x,y,meta)

def create_postprocessor(config):

    def normalize(T):
        x,y,meta = T
        if config['NORMALIZE'] == 'MEAN':
            x = (1.0*x-meta['MEAN'])/meta['STD']

        if config['NORMALIZE'] == 'MAX':
            x = (1.0*x-np.amin(x))/(np.amax(x)-np.amin(x))

        x = x.reshape([1]+x.shape)

        return (x,y,meta)
    return normalize

def get_yamls(data_dir):
    l = os.listdir(data_dir)
    l = [f for f in l if '.yaml' in f]
    l = [io_.load_yaml(data_dir+'/'+f) for f in l]
    return l
