from gml_models.gaussian import ConditionalGaussian, GaussianLogger
from gml_processors.dictionaryProcessor import DictionaryProcessor, VecToDictProcessor
from gml_datasets.dataset import RandomDataset, MappedDataset, ThreadDataset, IDListDataset, LRMappedDataset
from gml_io.io import save_json, load_json, configure_dirs, upsert_dirs
from gml_graph.graph import Graph
from gml_apps.apps import GMLApp
from gml_metrics.metrics import absError, stdRelativeErrorMissing, l2Error
from gml_util.train import train
from gml_evaluations.evaluation import dropFields
from gml_logging.logger import LossLogger

from tqdm import tqdm
import os
import numpy as np

"""
1. initialize model
2. get preprocessors
3. hook up in graph
4. make app
5. (if train) make reader and datasets
"""

def get_app(base_dir, config, mode="TRAIN"):
    config = configure_dirs(base_dir, config)

    config['FEATURE_DESCRIPTOR_FILE'] = os.path.join(base_dir,\
        config['FEATURE_DESCRIPTOR_FILE'])

    features_descriptor    = load_json(config['FEATURE_DESCRIPTOR_FILE'])
    config['NUM_FEATURES'] = len(features_descriptor.keys())

    #Set up pre and post processor
    preprocessor = DictionaryProcessor()
    preprocessor.load(config['FEATURE_DESCRIPTOR_FILE'])

    postprocessor = VecToDictProcessor()
    postprocessor.load(config['FEATURE_DESCRIPTOR_FILE'])

    config['NUM_PROCESSED_FEATURES'] = preprocessor.numProcFeats

    #build model
    model = ConditionalGaussian(config['ALPHA'],\
        config['NUM_PROCESSED_FEATURES'])

    #Build graph
    graph = Graph()
    graph.add_node(name='X')
    graph.add_node(preprocessor.process, name='Xnorm', depends={'X':'d'})
    graph.add_node(model.predict, name='P', depends={'Xnorm':'x'})
    graph.add_node(model.confidence, name='Confidence', depends={'Xnorm':'x'})
    graph.add_node(model.train, name='Train', depends={'Xnorm':'x'})

    graph.add_node(postprocessor.process, name='Prediction', depends={'P':'x'})

    #Build app
    App = GMLApp()
    App.setPredict( lambda x: graph.get('Prediction', {"X": x}) )
    App.setLoad( lambda: model.load(config['MODEL_DIRECTORY']) )
    App.setSave( lambda: model.save(config['MODEL_DIRECTORY']) )
    App.setModel(model)

    preprocess_func = lambda x: graph.get('Xnorm', {'X': x} )
    for d in config['DIR_KEYS']: upsert_dirs(config[d])

    if mode == "TRAIN":

        train_files = os.listdir(config['DATA_DIRECTORY'])
        train_files = [config['DATA_DIRECTORY']+'/'+s for s in train_files]
        train_set   = RandomDataset(train_files, load_json)
        processed_set = MappedDataset(train_set, preprocess_func)

        test_files = os.listdir(config['TEST_DIRECTORY'])[:config['TEST_ITERATIONS']]
        test_files = [config['TEST_DIRECTORY']+'/'+s for s in test_files]
        test_set   = IDListDataset(test_files, load_json)

        drop_set = MappedDataset(test_set,
            lambda x: dropFields(x,2))

        processed_drop_set = MappedDataset(drop_set, preprocess_func)

        App.setDataset(test_set, 'TEST')

        processed_test_set = MappedDataset(test_set, preprocess_func)

        test_std = np.std(np.array([a for a in processed_test_set.get()]),axis=0)

        App.setDataset(processed_test_set, "PROCESSED_TEST")

        train_logger = GaussianLogger(model, processed_set.get(), key='TRAIN',\
            metric=absError, stats_iters=config['TEST_ITERATIONS'])
        test_logger  = GaussianLogger(model, processed_test_set.get(), key='TEST',\
            metric=absError, stats_iters=config['TEST_ITERATIONS'])

        test_loss_logger = LossLogger(model.predict,
            X=[a for a in processed_drop_set],
            Y=[a for a in processed_test_set.get()],
            metric = lambda x,y: stdRelativeErrorMissing(x,y, test_std),
            key='TEST ABS STD ERROR')

        loggers = [train_logger, test_logger, test_loss_logger]

        train_step = lambda x: graph.get('Train', {'Xnorm': x} )

        App.setTrain(lambda: train(train_step, processed_set,\
            config['TRAIN_ITERATIONS'], loggers, print_every=config['EVAL_STEP']))

    return App
