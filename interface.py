class AbstractExperiment(object):
    def __init__(self,config):
        raise RuntimeError("abstract not implemented")
    def load(self,config):
        raise RuntimeError("abstract not implemented")
    def predict(self):
        raise RuntimeError("abstract not implemented")
    def train(self):
        raise RuntimeError("abstract not implemented")
    def evaluate(self):
        raise RuntimeError("abstract not implemented")
    def store(self):
        raise RuntimeError("abstract not implemented")
        
class AbstractModel(object):
    def __init__(self,config):
        raise RuntimeError("abstract not implemented")
    def predict(self,T):
        raise RuntimeError("abstract not implemented")
    def save(self, filename):
        raise RuntimeError("abstract not implemented")
    def load(self, filename):
        raise RuntimeError("abstract not implemented")
    def train(self, T):
        raise RuntimeError("abstract not implemented")

class AbstractDataset(object):
    def __init__(self,config):
        raise RuntimeError("abstract not implemented")
    def next(self):
        raise RuntimeError("abstract not implemented")
