import os
from gml.gml_io.io import upsert_dirs
from gml.gml_dataset.dataset import RandomDataset, MappedDataset, ThreadDataset

def get_processors(basedir, config_key, config, G):
    processors = []
    for p in config[config_key]:
        p_name = p['NAME']
        p_fn   = os.path.join(base_dir, p['FILENAME'])

        proc   = G['Processors'][p_name]

        proc.load(p_fn)
        processors.append(proc)

    return processors

def make_train(file_list, reader, preprocessors, model, config):
    def train():
        train_set = RandomDataset(file_list, reader)
        for p in preprocessors:
            train_set = MappedDataset(train_set, p)
        train_set = ThreadDataset(train_set)

        for i in range(config['TRAIN_ITERATIONS']):
            #TODO: This isnt very general and can be improved
            x = train_set.next()
            model.train(x)
