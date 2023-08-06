import numpy as np

def joint(X):
    if X.shape[1] == 1:
       M = X
    else:
       Row = X.shape[0]
       M = np.zeros(shape = (Row, 1))
       count = 1
       M[0] = count
       curr = X[1, :]
       temp = X[0, :]
       if (temp == curr).all():
           M[1] = count
       else:
           count = count + 1
           M[1] = count
               
       for i in range(2, Row-1):
           curr = X[i, :]
           for j in range(0, i-1):
               temp = X[j, :]
               if (temp == curr).all():
                   M[i] = M[j]
#                   break
           if M[i] == 0:
               count = count + 1
               M[i] = count
    return M