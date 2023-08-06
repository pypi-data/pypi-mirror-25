from NormaliseArray import normaliseArray
import numpy as np

def mergeArrays(firstVector, secondVector, length):
    
    if length == 0:
        length = firstVector.size
    
    results = normaliseArray(firstVector, 0)
    firstNumStates = results[0]
    firstNormalisedVector = results[1]
    
    results = normaliseArray(secondVector, 0)
    secondNumStates = results[0]
    secondNormalisedVector = results[1]
    
    stateCount = 1
    stateMap = np.zeros(shape = (firstNumStates*secondNumStates,))
    merge = np.zeros(shape =(length,))
    
    for i in range(0, length):
        curIndex = firstNormalisedVector[i] + (secondNormalisedVector[i] * firstNumStates);
        if stateMap[int(curIndex)] == 0:
            stateMap[int(curIndex)] = stateCount
            stateCount = stateCount + 1
        merge[i] = stateMap[int(curIndex)]
    
    results = []
    results.append(stateCount)
    results.append(merge)
    
    return results