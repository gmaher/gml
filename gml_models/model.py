from gml.gml import GMLPlugin, registerPlugin

MODULE_NAME = "Models"

class Models(type, metaclass=GMLPlugin):
    def __new__(cls, name, bases, attrs):
        registerPlugin(MODULE_NAME, Models, cls, name, bases, attrs)
        return super(Models, cls).__new__(cls, name, bases, attrs)

class Model(object):
    def predict(self, x):
        raise RuntimeError("abstract")
    def train(self, x):
        raise RuntimeError("abstract")
    def save(self, output_dir):
        raise RuntimeError("abstract")
    def load(self, input_dir):
        raise RuntimeError("abtract")
