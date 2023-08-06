import numpy as np

def checkDataSize(X, T, S):

    # check enough data is valid for independence tests
    # at time 5 times the degree of freedom
    datasizeFlag = 0
    alpha = 5

    Xcard = np.unique(X).size
    Tcard = np.unique(T).size

    # check data size
    Scard = np.unique(S)
    [a, b] = np.histogram(S, Scard)
    #% all has to be fit data
    if min(a) < alpha * Xcard * Tcard:
        datasizeFlag = 1
    return datasizeFlag