from calculateJointProbability import JointProbability
from math import log

def ConditionalEntropy(dataVector, conditionVector, length):
    
    condEntropy = 0
    jointValue = 0
    condValue = 0
    
    if length == 0:
        length = dataVector.size
    
    results = JointProbability(dataVector, conditionVector, 0)
    
    jointProbabilityVector = results[0]
    numJointStates = results[1]
    #firstProbabilityVector = results[2]
    numFirstStates = results[3]
    secondProbabilityVector = results[4]
    #numSecondStates = results[5]
    
    for i in range(0, numJointStates):
        jointValue = jointProbabilityVector[i]
        condValue = secondProbabilityVector[int(i / numFirstStates)]
        if jointValue > 0 and condValue > 0:
            condEntropy -= jointValue * log(jointValue / condValue);
        
    condEntropy /= log(2)
    return condEntropy