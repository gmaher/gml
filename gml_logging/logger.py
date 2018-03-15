import numpy as np

class Logger(object):
    def __init__(self):
        raise RuntimeError("abstract not implemented")
    def log(self, iteration):
        raise RuntimeError("abstract not implemented")
    def setLog(self, log):
        self.log = log

class LossLogger(Logger):
    def __init__(self, predict, X, Y, metric, key, num_samples=1000, min_iters=1000):
        self.predict = predict
        self.X        = X
        self.Y        = Y
        self.metric   = metric
        self.key      = key
        self.num_samples = num_samples
        self.N           = len(X)
        self.min_iters   = min_iters

    def calculateError(self):
        indexes = np.random.choice(self.N, size=self.num_samples)
        Yhat    = [self.predict(self.X[i]) for i in indexes]
        Yt      = [self.Y[i] for i in indexes]

        for i in range(10):
            print(i)
            print(self.X[indexes[i]])
            print(Yt[i])
            print(Yhat[i])

        errs    = [self.metric(Yt[i], Yhat[i]) for i in range(len(Yhat))]
        err_mean = np.mean(errs)
        err_std  = np.std(errs)
        return err_mean, err_std

    def log(self, iteration):
        if iteration>self.min_iters:
            err_mean, err_std = self.calculateError()
            print("iteration {}: - {} - MEAN {}, STD {}".format(iteration, self.key,
                err_mean, err_std))

class TensorCILogger(LossLogger):
    def log(self, iteration):
        err_mean, err_std = self.calculateError()
        #tensorCIlog stuff
