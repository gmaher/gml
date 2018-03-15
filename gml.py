G = {}

def registerPlugin(module_name, module_class, cls, name, bases, attrs):
    if name in G[module_name]:
        raise RuntimeError("gml module {} plugin {} already exists"\
            .format(module_name, name))
    else:
        print("registering {} plugin {}".format(module_name, name))
        G[module_name][name] = \
            super(module_class, cls).__new__(cls, name, bases, attrs)

class GMLPlugin(type):
    def __new__(cls, name, bases, attrs):
        if not name in G:
            G[name] = {}
            print("Registering module {}".format(name))
            return super(GMLPlugin, cls).__new__(cls, name, bases, attrs)
