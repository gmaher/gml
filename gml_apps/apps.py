class GMLApp(object):
    def __init__(self):
        self.datasets = {}
    def setModel(self, model):
        self.model = model
    def setTrain(self, train):
        self.train   = train
    def setTrainStep(self, trainStep):
        self.trainStep = trainStep
    def setPredict(self, predict):
        self.predict = predict
    def setWrite(self, write):
        self.write = write
    def setEvaluate(self, evaluate):
        self.evaluate = evaluate
    def setLoad(self, load):
        self.load = load
    def setSave(self, save):
        self.save = save
    def setDataset(self, dataset, key):
        self.datasets[key] = dataset
    def getDataset(self, key):
        return self.datasets[key]
