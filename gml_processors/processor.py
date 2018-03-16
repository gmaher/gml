from gml.gml import GMLPlugin, registerPlugin

MODULE_NAME = "Processors"

class Processors(type, metaclass=GMLPlugin):
    def __new__(cls, name, bases, attrs):
        registerPlugin(MODULE_NAME, Processors, cls, name, bases, attrs)
        return super(Processors, cls).__new__(cls, name, bases, attrs)

class Processor(object):
    def process(self, x):
        raise RuntimeError("abstract")
    def train(self, x):
        pass
    def save(self, output_dir):
        raise RuntimeError("abstract")
    def load(self, input_dir):
        raise RuntimeError("abstract")
