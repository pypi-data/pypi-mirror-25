import numpy as np
import scipy.io

def tian_readData2(name, sample_size, ind):

    data = []
    mat = scipy.io.loadmat('breastEW.mat')
    
    [nsample, ndim] = data.shape
    
    
    if ind == 10:
        train_index = [1:math.floor(nsample/4), (math.floor(nsample*3/4)+ 1):nsample]
        trainD = data(train_index, :)
        trainL = labels(train_index)
    else:
        train_index = 1:math.floor(nsample * (1 - sample_size));
        trainD = data(train_index, :);
        trainL = labels(train_index);
    
    test_index = np.setdiff1d(1:nsample, train_index)
    
    testD = data(test_index, :)
    testL = labels(test_index)
    
    result = []
    result.append(trainD)
    result.append(trainL)
    result.append(testD)
    result.append(testL)
    
    return result