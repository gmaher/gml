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

class Node(object):
    def __init__(f, input_nodes, name):
        self.input_nodes = input_nodes
        self.f = f
        self.name = name

        if type(input_nodes) == list:
            if any([not type(n) == Node for n in input_nodes]):
                raise RuntimeError("One or more specified input nodes is not of type  Node")
            self.get_output = _multi_get_output
        elif type(input_nodes) == Node:
            self.get_output = _get_single_output
        else:
            raise RuntimeError("Input node is not of type Node")

    def _multi_get_output(self):
        inputs = [n.get_output() for n in self.input_nodes]
        return self.f(inputs)
    def _get_single_output(self):
        return self.f(self.input_nodes.get_output())
