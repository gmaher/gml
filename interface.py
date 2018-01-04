class AbstractExperiment(object):
    def __init__(self,trainer,predictor,evaluator):
        self.trainer     = trainer
        self.predictor   = predictor
        self.evaluator   = evaluator

    def predict(self):
        self.predictor.predict()

    def train(self):
        self.trainer.train()

    def evaluate(self):
        self.evaluator.predict()

class AbstractModel(object):
    def __init__(self):
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
    def __init__(self):
        raise RuntimeError("abstract not implemented")
    def next(self):
        raise RuntimeError("abstract not implemented")

class AbstractTrainer(object):
    def __init__(self, model, dataset):
        self.model   = model
        self.dataset = dataset

    def train(self):
        while not self.dataset.done:
            T = self.dataset.next()
            self.model.train(T)

class AbstractPredictor(object):
    def __init__(self, model, dataset, store_fn):
        self.model   = model
        self.dataset = dataset
        self.store   = store_fn

    def predict(self):
        while not self.dataset.done:
            T = self.dataset.next()
            P = self.model.predict(T)
            self.store(T,P)
