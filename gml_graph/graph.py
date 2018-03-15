import inspect

def input_node(self):
    if self.output == None:
        raise RuntimeError("node {} is an input node but no input supplied".format(self.name))

class Graph(object):
    def __init__(self):
        self.nodes = {}

    def add_node(self,n=input_node,name="node",depends={}, fixed_params={}):

        self.check_inputs(n,name,depends)

        input_nodes = {}
        for k in depends:
            input_nodes[k] = self.nodes[k]

        if callable(n):
            node = Node(n,name, fixed_params=fixed_params)
        else:
            node = n

        node.set_input_nodes(input_nodes,depends)

        self.nodes[name] = node

    def get(self, name, input_dict={}):
        if type(name) == list or type(name) == tuple:
            return self.get_list(name, input_dict)

        self.check_get_inputs(name, input_dict)

        for k in input_dict.keys():
            self.nodes[k].set_output(input_dict[k])

        o = self.nodes[name].get_output()

        for k in self.nodes.keys():
            self.nodes[k].reset()

        return o

    def get_list(self, names, input_dict={}):
        for n in names:
            self.check_get_inputs(n, input_dict)

        for k in input_dict.keys():
            self.nodes[k].set_output(input_dict[k])

        outs = []
        for n in names:
            o = self.nodes[n].get_output()
            outs.append(o)

        for k in self.nodes.keys():
            self.nodes[k].reset()

        return outs

    def check_inputs(self, f, name, depends):
        if name in self.nodes:
            raise RuntimeError("node with name {} already exists".format(name))

        for k in depends:
            if not k in self.nodes:
                raise RuntimeError("node with name {} declared as dependency for {} but does not exist".format(k,name))

    def check_get_inputs(self,name,input_dict):
        for k in input_dict.keys():
            if not k in self.nodes:
                raise RuntimeError("Node with name {} supplied as input but does not exist".format(k))

        if not name in self.nodes:
            raise RuntimeError("output for Node with name {} requested, but does not exist".format(name))

class Node(object):
    def __init__(self, f, name, fixed_params={}):
        self.input_nodes = {}
        self.input_map  = {}
        self.f = f
        self.name = name
        self.recompute = True
        self.fixed_params = fixed_params

    def set_input_nodes(self, nodes, map_):
        """
        nodes - dictionary of nodes (nodes.keys() in keys)
        keys  - list of keys, determines the input ordering
        """
        self.input_map  = map_
        self.input_nodes = nodes

    def get_output(self):
        if self.recompute:
            if len(self.input_map.keys()) == 0 and\
                len(self.fixed_params.keys()) == 0:
                self.output = self.f()
            else:
                inputs = {}
                for n_name in self.input_map.keys():
                    arg_name = self.input_map[n_name]
                    arg_val = self.input_nodes[n_name].get_output()
                    inputs[arg_name] = arg_val

                for k in self.fixed_params.keys(): inputs[k] =\
                    self.fixed_params[k]

                self.output = self.f(**inputs)

        self.recompute = False
        return self.output

    def set_output(self,x):
        self.recompute=False
        self.output = x

    def reset(self):
        self.recompute = True
