# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 19:39:37 2017

@author: Keyi Liu
"""
from os import path
from sklearn import preprocessing
import pandas as pd
import numpy as np
import json
# import stmb_python_primitive
# from stmb_python_primitive import STMBFeatureSelector
# from stmb_python_primitive import *
import STMBFeatureSelector
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# Load the json configuration file
with open("ta1-pipeline-config.json", 'r') as inputFile:
    jsonCall = json.load(inputFile)
    inputFile.close()
    
# Load the json dataset description file
with open(jsonCall['dataset_schema'], 'r') as inputFile:
    datasetSchema = json.load(inputFile)
    inputFile.close()
    
dataRoot = jsonCall['data_root']
trainData = pd.read_csv( path.join(dataRoot, 'trainData.csv'), header=0).fillna('0').replace('', '0')
trainTargets = pd.read_csv( path.join(dataRoot, 'trainTargets.csv'), header=0).fillna('0').replace('', '0')
testData = pd.read_csv( path.join(dataRoot, 'testData.csv'), header=0).fillna('0').replace('', '0')
print ('\nData preprocessing phase start ......')

'''
The first step is the data cleaning and the data preprocessing, this session of code can be replaced by other
TA1's primitives that doing similar jobs, the input of our algorithm should be numpy array with numerical values
'''

# Encode the categorical data in training data, and discretize the numerical data
trainDataCatLabels = []
trainDataLabelEncoders = dict()

trainDataNumLabels = []
trainDataNumBins = dict()

for colDesc in datasetSchema['trainData']['trainData']:
    if colDesc['varType']=='categorical':
        trainDataCatLabels.append(colDesc['varName'])
        trainDataLabelEncoders[colDesc['varName']] = preprocessing.LabelEncoder().fit(trainData[colDesc['varName']])
        trainData[colDesc['varName']] = trainDataLabelEncoders[colDesc['varName']].transform(trainData[colDesc['varName']])
    '''    
    if colDesc['varType'] == 'integer' or colDesc['varType'] == 'float':
        # unique values less then 10
        trainDataNumLabels.append(colDesc['varName'])
        if len(np.unique(trainData[colDesc['varName']].astype(np.float64))) > 10:
            min_val = np.amin(trainData[colDesc['varName']].astype(np.float64))
            max_val = np.amax(trainData[colDesc['varName']].astype(np.float64))
            bins = np.linspace(min_val, max_val, 10)
            trainDataNumBins[colDesc['varName']] = bins
            trainData[colDesc['varName']] = np.digitize(trainData[colDesc['varName']].astype(np.float64), trainDataNumBins[colDesc['varName']])
        
        else:
            trainDataLabelEncoders[colDesc['varName']] = preprocessing.LabelEncoder().fit(trainData[colDesc['varName']].astype(np.float64))
            trainData[colDesc['varName']] = trainDataLabelEncoders[colDesc['varName']].transform(trainData[colDesc['varName']].astype(np.float64))
     '''   
        
trainD = trainData.as_matrix().astype(np.float64)[:, 1:] 



# Encode the categorical data in the test targets, uses the first target of the dataset as a target
trainTargetsCatLabel = ''
trainTargetsLabelEncoder = preprocessing.LabelEncoder()
for colDesc in datasetSchema['trainData']['trainTargets']:
    if colDesc['varType']=='categorical':
        trainTargetsCatLabel = colDesc['varName']
        trainTargetsLabelEncoder = trainTargetsLabelEncoder.fit(trainTargets[colDesc['varName']])
        trainTargets = trainTargetsLabelEncoder.transform(trainTargets[colDesc['varName']])
    if colDesc['varRole']=='target':
        break

trainT = trainTargets

# Encode the testData using the previous label encoders and bins
for colLabel in trainDataCatLabels:
    testData[colLabel] = trainDataLabelEncoders[colLabel].transform(testData[colLabel])

'''
for colLabel in trainDataNumLabels:
    if colLabel in trainDataLabelEncoders.keys():
        testData[colLabel] = trainDataLabelEncoders[colLabel].transform(testData[colLabel].astype(np.float64))
    else:
        testData[colLabel] = np.digitize(testData[colLabel].astype(np.float64), trainDataNumBins[colLabel])
'''


testD = testData.as_matrix().astype(np.float64)[:, 1:]


print ('Generateing Inputs: data and labels .....')
print (trainD.shape)
print (trainT.shape)
print ('\n')

"""
Here, we separate the training data and the testing data
"""
X_train, X_test, y_train, y_test = train_test_split(trainD, trainT, test_size=0.33)


"""
Fit the feature selection model 
then make predictions to the training and testing data, the output Z is the dimensionality reduced testing data, 
and the X = stmb.predict(X_train) is the dimensionality reduced training data
"""
print ('Training phase: applying STMB feature selection primitive ......')
print ('Number of selected features: ')
stmb = STMBFeatureSelector.STMBFeatureSelector()
stmb.set_training_data(X_train, y_train)
stmb.fit()
X = stmb.produce(X_train)
Z = stmb.produce(X_test)

enhanced_realtest = stmb.produce(testD)


"""
Fit the KNN classifier, and 
compute the classification accuracy
"""
print ('Classification phase: sklearn KNN classifier')
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y_train)
pred = knn.predict(Z)

print(accuracy_score(y_test, pred))
predictedTargets = knn.predict(enhanced_realtest)

print ('Save the predicted labels for the testing data.\n')

with open(jsonCall['output_file'], 'w') as outputFile:
    output = pd.DataFrame(predictedTargets).to_csv(outputFile, index_label='d3mIndex', header=[trainTargetsCatLabel])









