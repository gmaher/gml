from gml_models.model import Models, Model

import numpy as np
EPS = 1e-5
class ConditionalGaussian(Model, metaclass=Models):
    def __init__(self, alpha, n_features):
        self.alpha      = alpha
        self.n_features = n_features

        self.mean = np.zeros((n_features))
        self.variance  = np.ones((n_features))
        self.covariance = np.zeros((n_features, n_features))
        self.correlation = np.zeros((n_features, n_features))

        self.I = np.eye(n_features)

        self.init_mean = True
        #for i in range(n_features): self.correlation[i,i] = 1.0

    def predict(self, x):
        missing     = np.isnan(x)
        not_missing = ~np.isnan(x)

        B = self.correlation[missing,:]
        B = B[:,not_missing]

        C = self.correlation[not_missing, :]
        C = C[:,not_missing]

        mu1 = self.mean[missing]
        mu2 = self.mean[not_missing]
        x2  = x[not_missing]

        s1  = np.sqrt(self.variance[missing])
        s2  = np.sqrt(self.variance[not_missing])

        z2 = (x2-mu2)/s2

        v  = np.linalg.solve(C,z2)
        x1 = mu1 + B.dot(v)*s1

        x_imputed = np.zeros((self.n_features))
        x_imputed[missing] = x1
        x_imputed[not_missing] = x2

        return x_imputed

    def confidence(self, x):

        missing     = np.isnan(x)
        not_missing = ~np.isnan(x)

        A = self.correlation[missing,:]
        A = A[:,missing]

        B = self.correlation[missing,:]
        B = B[:,not_missing]

        C = self.correlation[not_missing, :]
        C = C[:,not_missing]
        CinvBT = np.linalg.solve(C,B.T)
        new_sig = A-B.dot(CinvBT)

        s = np.zeros((x.shape))
        s[missing] = np.diagonal(new_sig)
        s[not_missing] = 0.0
        s = s*self.variance
        return np.sqrt(np.abs(s))

    def train(self,x):

        not_missing = ~np.isnan(x)
        cov_indices =\
         not_missing[:,np.newaxis].dot(not_missing[:,np.newaxis].T)

        if self.init_mean:
            self.mean = x
            self.init_mean = False

        delta_old = (x-self.mean)

        self.mean[not_missing] = self.mean[not_missing] +\
            self.alpha*(delta_old[not_missing])

        delta_new = (x-self.mean)

        self.variance[not_missing] = (1.0-self.alpha)*self.variance[not_missing] + self.alpha*(delta_new[not_missing]*delta_new[not_missing])

        z1 = delta_old[:,np.newaxis]
        z2 = delta_new[:,np.newaxis]

        self.covariance[cov_indices] = (1.0-self.alpha)*self.covariance[cov_indices] +\
             self.alpha*(z2.dot(z2.T))[cov_indices]

        rho = (1.0/np.sqrt(self.variance))[:,np.newaxis]

        self.correlation[cov_indices] = self.covariance[cov_indices]*(rho.dot(rho.T))[cov_indices]

    def save(self, output_directory):
        np.save(output_directory+'mean.npy',self.mean)
        np.save(output_directory+'variance.npy',self.variance)
        np.save(output_directory+'covariance.npy',self.covariance)
        np.save(output_directory+'correlation.npy',self.correlation)

    def load(self, input_directory):
        self.mean = np.load(input_directory+'mean.npy')
        self.variance = np.load(input_directory+'variance.npy')
        self.covariance = np.load(input_directory+'covariance.npy')
        self.correlation = np.load(input_directory+'correlation.npy')

class GaussianLogger:
    def __init__(self, model, dataset, key, metric, stats_iters=10000):
        self.model   = model
        self.dataset = dataset
        self.key     = key
        self.metric  = metric

        examples = []
        print("getting stats for GaussianLogger {}".format(key))
        for i in range(stats_iters):
            d = self.dataset.next()
            examples.append(d)

        X = np.array(examples)

        self.MEAN = np.mean(X,axis=0)
        self.VAR  = np.var(X,axis=0)
        self.COV  = np.cov(X, rowvar=False)
        self.CORR = np.corrcoef(X, rowvar=False)

        self.ERRS               = {}
        self.ERRS['ITERATIONS'] = []
        self.ERRS['MEAN']       = []
        self.ERRS['VAR']        = []
        self.ERRS['COV']        = []
        self.ERRS['CORR']       = []

    def log(self, iteration):
        e_mean = self.metric(self.MEAN, self.model.mean)
        e_var  = self.metric(self.VAR, self.model.variance)
        e_cov  = self.metric(self.COV, self.model.covariance)
        e_corr = self.metric(self.CORR, self.model.correlation)

        self.ERRS['ITERATIONS'].append(iteration)
        self.ERRS['MEAN'].append(e_mean)
        self.ERRS['VAR'].append(e_var)
        self.ERRS['COV'].append(e_cov)
        self.ERRS['CORR'].append(e_corr)

        print(self.key, ": MEAN ", self.ERRS['MEAN'][-1], "VAR ", self.ERRS['VAR'][-1], "COV ", self.ERRS['COV'][-1], "CORR ", self.ERRS['CORR'][-1])
