import numpy as np

def normaliseArray(vector, length):
    minVal = 0
    maxVal = 0
    currentValue = 0
    
    if length == 0:
         length = vector.size
         
    normalised = np.zeros(shape = (length,))
    
    if length:
        minVal = int(np.floor(vector[0]))
        maxVal = int(np.floor(vector[0]))
        for i in range(0, length):
            currentValue = int(np.floor(vector[i]))
            normalised[i] = currentValue
            if currentValue < minVal:
                minVal = currentValue
            if currentValue > maxVal:
                maxVal = currentValue
                
        for i in range(0, length):
            normalised[i] = normalised[i] - minVal
            
        maxVal = (maxVal - minVal) + 1
        
    results = []
    results.append(maxVal)
    results.append(normalised)
    
    return results
    
             