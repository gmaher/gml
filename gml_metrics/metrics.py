import numpy as np

def stdRelativeError(truth, pred, std, eps=1e-5):
    E = np.mean(np.abs(1.0*pred-truth)/(std))
    return E

def stdRelativeErrorMissing(truth, pred, std, eps=1e-5):
    e = np.abs(1.0*pred-truth)
    E = np.mean(e[e>eps]/std[e>eps])
    return E

def l2Error(truth, pred, eps=1e-5):
    E = np.sum((1.0*pred-truth)**2)
    return E

def absError(truth, pred, eps=1e-5):
    E = np.sum(np.abs(1.0*pred-truth))
    return E
