from math import log
import numpy as np
from itertools import combinations
from sklearn.neighbors import KNeighborsClassifier

def JMI_BF(train_data, train_label):
    
    neigh = KNeighborsClassifier(n_neighbors = 3)
    
    featureSIZE = 1;
    
    noOfFeatures = train_data.shape[1]
    noOfSamples = train_data.shape[0]
    
    test_SampleSIZE = int(np.floor(noOfSamples/3))
    
    test_data = train_data[0:test_SampleSIZE, :]
    test_label = train_label[0:test_SampleSIZE]
    
    ERR_JMI = np.zeros(shape = (noOfFeatures,))
    
    features_JMI = JMI(noOfFeatures, noOfSamples, noOfFeatures, train_data, train_label)
    features_JMI = features_JMI.astype(int)
    
    feat = features_JMI[0:featureSIZE]
    neigh.fit(train_data[:, feat], train_label)

    ERR_JMI[0] = 1 - neigh.score(test_data[:,feat], test_label)
    
    MIN_ERR = ERR_JMI[0]
    MIN_SIZE = featureSIZE
    
    for featureSIZE in range(2, noOfFeatures):
        feat = features_JMI[0:featureSIZE]
        neigh.fit(train_data[:, feat], train_label)
        ERR_JMI[featureSIZE-1] = 1 - neigh.score(test_data[:, feat], test_label)
        
        if ERR_JMI[featureSIZE-1] < MIN_ERR:
            MIN_ERR = ERR_JMI[featureSIZE-1]
            MIN_SIZE = featureSIZE
            
    return features_JMI[0:MIN_SIZE]


def JMI(k, noOfSamples, noOfFeatures, featureMatrix, classColumn):
    
    classMI = np.zeros(shape = (noOfFeatures,))
    selectedFeatures = np.zeros(shape = (noOfFeatures,))
    
    sizeOfMatrix = k*noOfFeatures
    featureMIMatrix = np.zeros(shape = (sizeOfMatrix,))
    
    outputFeatures = np.zeros(shape = (k,))
    
    maxMI = 0
    maxMICounter = -1
    
    feature2D = [[]]*noOfFeatures
    
    for i in range(0, noOfFeatures):
        feature2D[i] = featureMatrix[:,i]
    
    for i in range(0, sizeOfMatrix):
        featureMIMatrix[i] = -1
        
    for i in range(0, noOfFeatures):
        classMI[i] = mi(feature2D[i], classColumn, noOfSamples)
        if classMI[i] > maxMI:
            maxMI = classMI[i]
            maxMICounter = i
    
    selectedFeatures[maxMICounter] = 1
    outputFeatures[0] = maxMICounter
    
    for i in range(1, k):
        score = 0
        currentHighestFeature = 0
        currentScore = 0
        #totalFeatureMI = 0
        
        for j in range(0, noOfFeatures):
            # if not select j
            if selectedFeatures[j] == 0:
                currentScore = 0
                #totalFeatureMI = 0                
                for x in range(0, i):
                    arrayPosition = x*noOfFeatures + j
                    
                    if featureMIMatrix[arrayPosition] == -1:
                        results = mergeArrays(feature2D[int(outputFeatures[x])], feature2D[j], noOfSamples)
                        mergedVector = results[1]
                        mutualinfo = mi(mergedVector, classColumn, noOfSamples)
                        featureMIMatrix[arrayPosition] = mutualinfo
                     
                    currentScore += featureMIMatrix[arrayPosition]
                     
                if currentScore > score:
                    score = currentScore
                    currentHighestFeature = j
                    
        selectedFeatures[currentHighestFeature] = 1
        outputFeatures[i] = currentHighestFeature
    
    return outputFeatures                         


def RecognizePC(targets, ADJt, data, THRESHOLD, NumTest):

    MIs = []
    NonPC = []
    cutSetSize = 0
    data_check = 1
    #targets = data[:, T]
    Sepset = [[]]*data.shape[1]
    #% Search
    datasizeFlag = 0
    while ADJt.size > cutSetSize:
        for xind in range(0, ADJt.size):        # for each x in ADJt
            X = ADJt[xind]
            if cutSetSize == 0:
                NumTest = NumTest + 1
                TEMP = mi(data[:, X], targets, 0)
                MIs.append([TEMP])   #compute mutual information               
                if TEMP <= THRESHOLD:
                     NonPC.append(X)              
            elif cutSetSize == 1: 
                Diffx = np.setdiff1d(ADJt, X)
                C = list(combinations(Diffx, cutSetSize))
                for sind in range(0, len(C)):                    # for each S in ADJT\x, size
                        S = np.array(list(C[sind]))
                        cmbVector = joint(data[:, S])
                        if data_check:
                            datasizeFlag = checkDataSize(data[:, X], targets, cmbVector)
                        if datasizeFlag != 1:
                            NumTest = NumTest + 1
                            TEMP = cmi(data[:, X], targets, cmbVector, 0)
                            MIs.append([TEMP])                          
                            if TEMP <= THRESHOLD:
                                NonPC = set(NonPC).union(set([X]))
                                Sepset[X] = set(Sepset[X]).union(set(S))
                                break
                        else:
                            break
            else:                                # set size > 1
                Diffx = np.setdiff1d(ADJt, X)                
                C = list(combinations(Diffx, cutSetSize - 1))
                midBreakflag = 0
                for sind in range(0, len(C)):             # for each S in ADJT\x, size
                    S = np.array(list(C[sind]))
                    RestSet = np.setdiff1d(Diffx, S); 
                    for addind in range(0, RestSet.size):
                        col = set(S).union(set([RestSet[addind]]))
                        cmbVector = joint(data[:, np.array(list(col))])
                        if data_check:
                            datasizeFlag = checkDataSize(data[:, X], targets, cmbVector)
                        if datasizeFlag != 1:
                            NumTest = NumTest + 1
                            TEMP = cmi(data[:, X], targets, cmbVector, 0)
                            MIs.append([TEMP])
                                             
                            if TEMP <= THRESHOLD:
                                NonPC = set(NonPC).union(set([X]))
                                Sepset[X] = set(Sepset(X)).union(set(S),set([RestSet(addind)]))
                                midBreakflag = 1
                                break                                                    
                        else:
                            break
                    if midBreakflag == 1:
                        break

        if len(NonPC) > 0:
           ADJt = np.setdiff1d(ADJt, NonPC)
           cutSetSize = cutSetSize + 1
           NonPC = []
        elif datasizeFlag == 1:
           break
        else:
           cutSetSize = cutSetSize + 1
    
    ADJ = ADJt
    
    result = []
    result.append(ADJ)
    result.append(Sepset)
    result.append(NumTest)
    result.append(cutSetSize)
    result.append(MIs)
    
    return result


def checkDataSize(X, T, S):

    # check enough data is valid for independence tests
    # at time 5 times the degree of freedom
    datasizeFlag = 0
    alpha = 5

    Xcard = np.unique(X).size
    Tcard = np.unique(T).size

    # check data size
    temp = np.unique(S)
    Scard = list(temp)
    Scard.append(np.max(temp)+1)
    Scard = np.array(Scard)
    
    [a, b] = np.histogram(S, Scard)
    #% all has to be fit data
    if min(a) < alpha * Xcard * Tcard:
        datasizeFlag = 1
    return datasizeFlag


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
               
       for i in range(2, Row):
           curr = X[i, :]
           for j in range(0, i):
               temp = X[j, :]
               if (temp == curr).all():
                   M[i] = M[j]
#                   break
           if M[i] == 0:
               count = count + 1
               M[i] = count
    return M


def cmi(dataVector, targetVector, conditionVector, length):
    cmi = 0
    firstCondition = 0
    secondCondition = 0
    
    if length == 0:
        length = dataVector.size
    
    results = mergeArrays(targetVector, conditionVector, length)
    mergedVector = results[1]
    
    firstCondition = ConditionalEntropy(dataVector, conditionVector, length)
    secondCondition = ConditionalEntropy(dataVector, mergedVector, length)
    
    cmi = firstCondition - secondCondition
    
    return cmi


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