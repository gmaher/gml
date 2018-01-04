import os
import sys
sys.path.append(os.path.abspath('../../'))
import io_
import numpy as np

from experiment import MNISTModel, get_yamls

config = io_.parse_config('config.yaml')

yamls  = get_yamls(config['DATA_DIR'])

train_yamls = [y for y in yamls if y['SET'] == 'TRAIN']

def read_example(yaml):
    x = np.load(yaml['x'])
    y = yaml['y']
    return x,y

def post_process_example(x,y):
    x     = (1.0*x)/255
    ym    = np.zeros((10))
    ym[y] = 1

    return x,ym

def get_batch(yamls,num_batch=4):
    X    = []
    Y    = []
    meta = []
    for i in range(num_batch):
        yaml = np.random.choice(yamls)

        x,y  = read_example(yaml)

        x,y  = post_process_example(x,y)

        X.append(x)
        Y.append(y)
        meta.append(yaml)

    X = np.asarray(X)
    Y = np.asarray(Y)
    return X,Y, meta

def train_connector(T):
    x,y,meta = T
    model.train(x,y)

def log_train(T):
    x,y,meta = T
    yhat = model.predict(x)
    l = np.sum(np.abs(yhat-y))
    print "loss = {}".format(l)

def store_prediction(p,yaml):
    print "prediction for {} is {}".format(yaml['id'],p)

def store_evaluation(x,p,y,yaml):
    id_ = yaml['id']
    e_mean = np.mean(np.abs(p-y))
    e_std  = np.std(p-y)
    e_abs  = np.sum(np.abs(p-y))
    print "mean error {} = {}".format(id_,e_mean)
    print "std error {} = {}".format(id_,e_std)
    print "abs error {} = {}".format(id_,e_abs)

##############
# Params
#############
train_iters = 1000

model = MNISTModel()

###########################
# Train
###########################
for i in range(train_iters):

    T = get_batch(train_yamls)

    train_connector(T)

    if i%100 == 0:
        log_train(T)

###########################
# predict
###########################
for yaml in train_yamls:
    x,y = read_example(yaml)
    x,y = post_process_example(x,y)
    x   = x.reshape([1]+list(x.shape))
    p   = model.predict(x)
    store_prediction(p,yaml)

##########################
# Evaluate
##########################
for yaml in train_yamls:
    x,y = read_example(yaml)
    x,y = post_process_example(x,y)
    x   = x.reshape([1]+list(x.shape))
    p   = model.predict(x)
    store_evaluation(x,p,y,yaml)
