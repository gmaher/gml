import numpy as np
from gml.gml_processors.processor import Processors, Processor
from gml.gml_io.io import load_json, save_json

class DictionaryProcessor(Processor, metaclass=Processors):
    def __init__(self):
        pass

    def save(self, filename):
        save_json(filename, self.features_descriptor)

    def load(self, filename):
        self.features_descriptor = load_json(filename)
        self.keys = sorted(self.features_descriptor.keys())
        self.numFeats = len(self.keys)
        self.getFeatureCounts()

    def getFeatureCounts(self):
        self.numProcFeats = 0
        self.featPositions = {}

        for k,v in self.features_descriptor.items():
            self.featPositions[k] = {}
            self.featPositions[k]['start'] = self.numProcFeats

            if v['type'] == 'number' or v['type'] == 'binary':
                self.numProcFeats+=1
            if v['type'] == 'categorical':
                self.numProcFeats+=len(v['values'])

            self.featPositions[k]['stop'] = self.numProcFeats

    def process(self,d):

        x = np.zeros((self.numProcFeats))
        d_copy = {}
        for k,v in d.items(): d_copy[k] = v
        for feature in self.keys:
            descriptor = self.features_descriptor[feature]
            feat_type  = descriptor['type']

            start = self.featPositions[feature]['start']
            stop  = self.featPositions[feature]['stop']

            if feat_type == "number":
                self.processNumber(x,d_copy,feature,start,stop)
            elif feat_type == "binary":
                self.processBinary(x,d_copy,feature,start,stop,\
                    descriptor)
            elif feat_type == "categorical":
                self.processCategorical(x,d_copy,feature,start,\
                    stop, descriptor)
            else:
                raise RuntimeError("Unrecognized feature type\
                    {}".format(feat_type))

        return x

    def processNumber(self,x,d,feature,start,stop):
        val = d[feature]
        if feature not in d:
            x[start] = None
        else:
            x[start] = d[feature]

    def processBinary(self,x,d,feature,start,stop,descriptor):
        if feature not in d:
            x[start] = None
        else:
            v = d[feature]
            on = descriptor['on_value']
            of = descriptor['off_value']
            if v == on:
                x[start] = 1.0
            else:
                x[start] = 0.0

    def processCategorical(self,x,d,feature,start,\
        stop,descriptor):
        if feature not in d:
            x[start:stop] = None
        else:
            v = d[feature]
            if not any([v == c for c in\
                descriptor['values']]):

                x[start:stop] = None

            else:
                index = [i for i in range(stop-start) if \
                    v == descriptor['values'][i]][0]

                x[start+index] = 1

class VecToDictProcessor(DictionaryProcessor):
    def process(self, x):
        d = {}

        for feature in self.keys:
            descriptor = self.features_descriptor[feature]
            feat_type  = descriptor['type']

            start = self.featPositions[feature]['start']
            stop  = self.featPositions[feature]['stop']

            if feat_type == "number":
                self.deprocessNumber(x,d,feature,start,stop, descriptor)
            elif feat_type == "binary":
                self.deprocessBinary(x,d,feature,start,stop,\
                    descriptor)
            elif feat_type == "categorical":
                self.deprocessCategorical(x,d,feature,start,\
                    stop, descriptor)
            else:
                raise RuntimeError("Unrecognized feature type\
                    {}".format(feat_type))

        return d

    def deprocessNumber(self, x, d, feature, start, stop, descriptor):
        d[feature] = x[start]

    def deprocessBinary(self, x, d, feature, start, stop, descriptor):
        binary     = x[start]
        d[feature] = binary

    def deprocessCategorical(self, x, d, feature, start, stop, descriptor):
        probs      = x[start:stop]
        values     = descriptor['values']
        prediction = {}
        for k,p in zip(values,probs): prediction[k] = p
        d[feature] = prediction
