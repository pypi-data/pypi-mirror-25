from calculateJointProbability import JointProbability
from math import log

def mi(dataVector, targetVector, length):
    mi = 0
    if length == 0:
        length = dataVector.size
        
    results = JointProbability(dataVector, targetVector, 0)
    
    jointProbabilityVector = results[0]
    numJointStates = results[1]
    firstProbabilityVector = results[2]
    numFirstStates = results[3]
    secondProbabilityVector = results[4]
    #numSecondStates = results[5]
    
    for i in range(0, numJointStates):
        firstIndex = i % numFirstStates
        secondIndex = i / numFirstStates
        a = jointProbabilityVector[i]
        b = firstProbabilityVector[int(firstIndex)]
        c = secondProbabilityVector[int(secondIndex)]
        if ( a>0  and  b>0  and  c>0 ):
            mi += a * log(a / b / c)
        
    mi /= log(2)
    return mi