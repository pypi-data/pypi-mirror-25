import numpy as np
from NormaliseArray import normaliseArray

def JointProbability(firstVector, secondVector, length):
    
    if length == 0:
         length = firstVector.size
    
    results = normaliseArray(firstVector, 0)
    firstNumStates = results[0]
    firstNormalisedVector = results[1]
    
    results = normaliseArray(secondVector, 0)
    secondNumStates = results[0]
    secondNormalisedVector = results[1]
    
    jointNumStates = firstNumStates * secondNumStates
    
    #max1 = int(np.max(firstNormalisedVector)) + 1
    #max2 = int(np.max(secondNormalisedVector)) + 1
    #max3 = int(max2*firstNumStates + max1) + 1
    
    firstStateCounts = np.zeros(shape = (firstNumStates,))
    secondStateCounts = np.zeros(shape = (secondNumStates,))
    jointStateCounts = np.zeros(shape = (jointNumStates,))
    
    firstStateProbs = np.zeros(shape = (firstNumStates,))
    secondStateProbs = np.zeros(shape = (secondNumStates,))
    jointStateProbs = np.zeros(shape = (jointNumStates,))
    
    for i in range(0, length):
        firstStateCounts[int(firstNormalisedVector[i])] +=1
        secondStateCounts[int(secondNormalisedVector[i])] +=1
        jointStateCounts[int(secondNormalisedVector[i]*firstNumStates + firstNormalisedVector[i])] +=1
        
    for i in range(0, firstNumStates):
        firstStateProbs[i] = firstStateCounts[i] / length
        
    for i in range(0, secondNumStates):
        secondStateProbs[i] = secondStateCounts[i] / length
        
    for i in range(0, jointNumStates):
        jointStateProbs[i] = jointStateCounts[i] / length
    
    results=[]
    results.append(jointStateProbs)
    results.append(jointNumStates)
    results.append(firstStateProbs)
    results.append(firstNumStates)
    results.append(secondStateProbs)
    results.append(secondNumStates)
    
    return results