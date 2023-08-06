#%% tian_STMB_new.m
import numpy as np
from tian_RecognizePC_faster import RecognizePC
from tian_checkDataSize import checkDataSize
from joint import joint
from entropy_estimators import cmi

def STMB(data, targetindex, threshold):
    NumTest = 0   
    numf = data.shape[1]  # feature number
    targets = data[:, targetindex]    # selected index data 
    # %% Recognize Target PC
    CanMB = np.setdiff1d(np.arange(numf), targetindex)    # candidates
    
    Results = RecognizePC(targetindex, CanMB, data, threshold, NumTest)
    
    PCD = Results[0]
    Sepset_t = Results[1]
    NumTest = Results[2]
    cutSetSize = Results[3]
    
    spouse = [[]]*numf
    #scores = []
    Des = [[]]*PCD.size
    datasizeFlag = 0
    #%% Find Markov blanket
    
    for yind in range(0, PCD.size):
        flag = 0
        y = PCD[yind]
        searchset = np.setdiff1d(CanMB, PCD)
        
        for xind in range(0, searchset.size):
            x = searchset[xind]
            col = set(Sepset_t[x]).union(set([y]))
            cmbVector =joint(data[:, np.array(list(col))])
            datasizeFlag = checkDataSize(data[:, x], targets, cmbVector)
            
            if datasizeFlag != 1:
                NumTest = NumTest + 1
                T = cmi(data[:, x], targets, cmbVector)[0]
                if T > threshold:                    # v structure             
                    temp = set(PCD).union(set([x]))
                    for s in np.setdiff1d(np.array(list(temp)), y): 
                        T = cmi(data[:, y], targets, data[:, s])[0]
                        if T < threshold:
                            temp = set(Des[yind]).union(set([y]))
                            Des[yind] = np.array(list(temp))
                            flag = 1; 
                            break
                        else:
                            temp = set(spouse[y]).union(set([x]))
                            spouse[y]= np.array(list(temp))

            if flag == 1:                            
               break
    
    PCD = np.setdiff1d(PCD, Des[:])

    #%% Shrink spouse
    NonS = []
    S = []

    for i in np.setdiff1d(np.arange(numf), PCD):
        spouse[i] = []   # empty                                     

    for y in np.arange(len(spouse)):
        if spouse[y]:
           S.append( y)    # Y has spouses
           # shrink
           spousecan = spouse[y]
           for sind in np.arange(spousecan.size):
               s = spousecan(sind)
               col = set(y).union(set(spousecan),set(PCD))
               cmbVector = joint(data[:, np.setdiff1d(np.array(list(col)), s)])
               datasizeFlag = checkDataSize(data[:, s], targets, cmbVector)
               if datasizeFlag != 1:
                  NumTest = NumTest + 1
                  T = cmi(data[:, s], targets, cmbVector)[0]
                  if T < threshold:
                     NonS = set(NonS).union(set([s]))
           spouse[y] = np.setdiff1d(spousecan, np.array(list(NonS)))
           NonS = []
                                                            
    b = [];
    for i in np.arange(len(spouse)):
         if spouse[i]:
             b = set(b).union(set(spouse[i]))
    # remove false spouse from PC
    M = PCD       # setdiff(PCD,S); % M has no spouses in PCD set
    PCsize = M.size
    testSet = set(S).union(set(b))
    #testSet = np.array(list(temp))
    C = np.zeros(shape = (PCsize, 1))
    for x in M:
       col = set(PCD).union(set(testSet))
       cmbVector = joint(data[:, np.setdiff1d(np.array(list(col)), x)])
       datasizeFlag = checkDataSize(data[:, x], targets, cmbVector)
       if datasizeFlag != 1:
            NumTest = NumTest + 1
            T = cmi(data[:, x], targets, cmbVector)[0]
            if T < threshold:
               PCD = np.setdiff1d(PCD, x)                                                                      
     
    PCsize2 =np.mean(C)
    MB = set(PCD).union(set(b))
    
    result = []
    result.append(np.array(list(MB)))
    result.append(PCD)
    result.append(spouse)
    result.append(NumTest)
    result.append(cutSetSize)
    result.append(PCsize)
    result.append(PCsize2)
    
    return result                                                                


