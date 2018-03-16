import tensorflow as tf

from gml.gml_models.model import Models, Model

import numpy as np
EPS = 1e-5
class TensorflowModel(Model, metaclass=Models):
    def __init__(self, config):
        self.config = config

        self.buildGraph()

        self.configureTrainer()

        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer)

    def predict(self, x):
        return self.sess.run(self.prediction,{self.x:x})

    def train(self,x,y):
        self.global_step = self.global_step+1

        if np.sum(np.isnan(xb)) > 0: return
        if np.sum(np.isnan(yb)) > 0: return

        self.sess.run(self.train,{self.x:xb,self.y:yb})

    def save(self):
        model_dir  = self.case_config['MODEL_DIR']
        model_name = self.case_config['MODEL_NAME']
        self.saver.save(
            self.sess,model_dir+'/{}'.format(model_name))

    def load(self, model_path=None):
        if model_path == None:
            model_dir  = self.case_config['MODEL_DIR']
            model_name = self.case_config['MODEL_NAME']
            model_path = model_dir + '/' + model_name
        self.saver.restore(self.sess, model_path)

    def buildGraph(self):
        raise RuntimeError("Abstract not implemented")

    def configureTrainer(self):
        LEARNING_RATE = self.global_config["LEARNING_RATE"]
        self.global_step = tf.Variable(0, trainable=False)
        boundaries = [5000, 10000, 15000]
        values = [LEARNING_RATE, LEARNING_RATE/10, LEARNING_RATE/100, LEARNING_RATE/1000]
        learning_rate = tf.train.piecewise_constant(self.global_step, boundaries, values)

        self.opt = tf.train.AdamOptimizer(learning_rate)
        self.train = self.opt.minimize(self.loss)
