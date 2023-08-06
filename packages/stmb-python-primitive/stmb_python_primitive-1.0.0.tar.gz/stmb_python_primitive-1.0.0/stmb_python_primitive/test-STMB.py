import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from tian_STMB_new import STMB

trainD = np.loadtxt('trainD.txt')
trainL = np.loadtxt('trainL.txt')
testD = np.loadtxt('testD.txt')
testL = np.loadtxt('testL.txt')

#trainD = np.loadtxt('trainD.txt')
#trainL = trainD[:, 0]
trainD = trainD[:, 1:]
print(trainD.shape)

trainD = np.hstack((trainD, trainL[:, None]))
print(trainD.shape)
c = np.amax(trainL)
k = trainD.shape[1]
# testD = np.loadtxt('testD.txt')
# testL = np.loadtxt('testL.txt')

# labelindex = 0
# featuindex = np.setdiff1d(np.arange(k), labelindex)
# neigh = KNeighborsClassifier(n_neighbors = 3)

#%% compute KNN accuracy with all features
# features_ALL = featuindex
# neigh.fit(trainD[:,features_ALL], trainL)

# score_ALL = neigh.score(testD[:,features_ALL], testL)

#%% compute STMB 
thres = 0.5
Results = STMB(trainD, k - 1, thres)
features_STMB = Results[0]

print (features_STMB)
print (features_STMB.shape)

# %% compute KNN accuracy with STMB features
# neigh.fit(trainD[:, features_STMB], trainL)

# score_STMB = neigh.score(testD[:, features_STMB], testL)
# print(score_STMB)