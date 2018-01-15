import inspect

def input_node(self):
    if self.output == None:
        raise RuntimeError("node {} is an input node but no input supplied".format(self.name))

class Graph(object):
    def __init__(self):
        self.nodes = {}

    def add_node(self,n=input_node,name="node",depends=[]):

        self.check_inputs(n,name,depends)

        input_nodes = {}
        for k in depends:
            input_nodes[k] = self.nodes[k]

        if callable(n):
            node = Node(n,name)
        else:
            node = n

        node.set_input_nodes(input_nodes,depends)

        self.nodes[name] = node

    def get(self, name, input_dict={}):
        self.check_get_inputs(name, input_dict)

        for k in input_dict.keys():
            self.nodes[k].set_output(input_dict[k])

        o = self.nodes[name].get_output()

        for k in input_dict.keys():
            self.nodes[k].reset()

        return o

    def check_inputs(self, f, name, depends):
        if self.nodes.has_key(name):
            raise RuntimeError("node with name {} already exists".format(name))

        for k in depends:
            if not self.nodes.has_key(k):
                raise RuntimeError("node with name {} declared as dependency for {} but does not exist".format(k,name))

    def check_get_inputs(self,name,input_dict):
        for k in input_dict.keys():
            if not self.nodes.has_key(k):
                raise RuntimeError("Node with name {} supplied as input but does not exist".format(k))

        if not self.nodes.has_key(name):
            raise RuntimeError("output for Node with name {} requested, but does not exist".format(name))

class Node(object):
    def __init__(self, f, name):
        self.input_nodes = {}
        self.input_keys  = []
        self.f = f
        self.name = name
        self.output = None

    def set_input_nodes(self, nodes, keys):
        """
        nodes - dictionary of nodes (nodes.keys() in keys)
        keys  - list of keys, determines the input ordering
        """
        self.input_keys  = keys
        self.input_nodes = nodes

    def get_output(self):
        if self.output == None:
            if len(self.input_keys) == 0:
                return self.f()
            else:
                inputs = [self.input_nodes[k].get_output()\
                    for k in self.input_keys]

                return self.f(*inputs)
        else:
            return self.output

    def set_output(self,x):
        self.output = x

    def reset(self):
        self.output = None
