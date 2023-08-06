from math import log
import numpy as np
from itertools import combinations
from sklearn.neighbors import KNeighborsClassifier

def Auto_JMIplusSTMB(train_data, train_label):
    noOfFeatures = train_data.shape[1]
    noOfSamples = train_data.shape[0]
    
    test_SampleSIZE = int(np.floor(noOfSamples/3))
    
    test_data = train_data[0:test_SampleSIZE, :]
    test_label = train_label[0:test_SampleSIZE]
     
    neigh = KNeighborsClassifier(n_neighbors = 3)
    
    neigh.fit(train_data, train_label)
    score_ALL = neigh.score(test_data, test_label)
 
    #%% find percentage for JMI feature selection
    featureSIZE = int(np.ceil(0.5*noOfFeatures))
    
    features_JMI = JMI(noOfFeatures, noOfSamples, noOfFeatures, train_data, train_label)
    features_JMI = features_JMI.astype(int) 
    
    feat_S = features_JMI[0:featureSIZE]
    neigh.fit(train_data[:, feat_S], train_label)   
    score_JMI_S = neigh.score(test_data[:,feat_S], test_label)
    #MIN_SIZE = featureSIZE
    
    featureSIZE = featureSIZE + 1
    feat_B = features_JMI[0:featureSIZE]
    neigh.fit(train_data[:, feat_B], train_label)
    score_JMI_B = neigh.score(test_data[:,feat_B], test_label)
    
    while ( featureSIZE < noOfFeatures and (score_JMI_B > score_JMI_S or score_JMI_S + 0.001 < score_ALL)):
        score_JMI_S = score_JMI_B
        feat_S = feat_B
        #MIN_SIZE = featureSIZE
        featureSIZE = featureSIZE + 1
        feat_B = features_JMI[0:featureSIZE]
        neigh.fit(train_data[:, feat_B], train_label)
        score_JMI_B = neigh.score(test_data[:, feat_B], test_label)
    
    sub_train_data = train_data[:, feat_S]
    sub_test_data = test_data[:, feat_S]
    
    #%% automatically select threshold for STMB
    SearchRange = 0.1
    thres_smaller = SearchRange/4
    thres_bigger = 3*SearchRange/4
    
    Picked = np.zeros(shape = (3,))
    features_picked = []
    
    Max = np.zeros(shape = (3,))
    features_max = []
    
    score_thresS = 0
    score_thresB = 0
    loop = 0
    
    while loop < 3 and ((Max[0] - score_ALL) < 0.01 or (1 - Max[0]) > 0.02):
            loop = loop + 1          
            step = SearchRange/pow(2,2+loop)
            
            #%% JMI + STMB
            Results = STMB(sub_train_data, train_label, thres_smaller)
            features_thresS = Results[0]
            features_thresS = features_thresS.astype(int) 
            
            Results = STMB(sub_train_data, train_label, thres_bigger)
            features_thresB = Results[0]
            features_thresB = features_thresB.astype(int) 
            
            if features_thresS.size != 0:
                neigh.fit(sub_train_data[:,features_thresS], train_label)
                score_thresS = neigh.score(sub_test_data[:, features_thresS], test_label)
                NF_thresS = features_thresS.size
            else:
                score_thresS = 0
                NF_thresS = 1e5
                
            if features_thresB.size != 0:
                neigh.fit(sub_train_data[:, features_thresB], train_label)
                score_thresB = neigh.score(sub_test_data[:, features_thresB], test_label)
                NF_thresB = features_thresB.size
            else:
                score_thresB = 0
                NF_thresB = 1e5
            
            index = np.argmax([Max[0], Picked[0], score_thresS, score_thresB])
            #%% record values
            if index == 1:
                Max[0] = Picked[0]
                Max[1] = Picked[1]
                Max[2] = Picked[2]
                features_max = features_picked
                
            elif index == 2:
                Max[0] = score_thresS
                Max[1] = NF_thresS
                Max[2] = thres_smaller
                features_max = features_thresS
                
            elif index == 3:
                Max[0] = score_thresB
                Max[1] = NF_thresB
                Max[2] = thres_bigger
                features_max = features_thresB
            #%% choose next search range
            if score_thresB - score_thresS > 0.001:
                Picked[0] = score_thresB
                Picked[1] = NF_thresB
                Picked[2] = thres_bigger
                features_picked = features_thresB
                thres_smaller = thres_bigger - step
                thres_bigger = thres_bigger + step
            
            elif score_thresS - score_thresB > 0.001:
                Picked[0] = score_thresS
                Picked[1] = NF_thresS
                Picked[2] = thres_smaller
                features_picked = features_thresS
                thres_bigger = thres_smaller + step
                thres_smaller = thres_smaller - step
                
            else:
                if NF_thresS > NF_thresB:
                    Picked[0] = score_thresB
                    Picked[1] = NF_thresB
                    Picked[2] = thres_bigger
                    features_picked = features_thresB
                    thres_smaller = thres_bigger - step
                    thres_bigger = thres_bigger + step
                else:
                    Picked[0] = score_thresS
                    Picked[1] = NF_thresS
                    Picked[2] = thres_smaller
                    features_picked = features_thresS
                    thres_bigger = thres_smaller + step
                    thres_smaller = thres_smaller - step
             #%% reset
            if features_thresS.size == 0 and features_thresB.size == 0:
                 SearchRange = SearchRange/2
                 thres_smaller = SearchRange/4
                 thres_bigger = 3*SearchRange/4
                 loop = 0
                 Picked = np.zeros(shape = (3,))
                 Max = np.zeros(shape = (3,))
                 features_picked = []
                 features_max = []
                 score_thresS = 0
                 score_thresB = 0
                 
    features = features_max
    
    return features


def STMB(train_data, targets, threshold):
    NumTest = 0   
    numf = train_data.shape[1]  # feature number
    #targets = data[:, targetindex]    # selected index data 
    # %% Recognize Target PC
    CanMB = np.arange(numf)    # candidates
    
    Results = RecognizePC(targets, CanMB, train_data, threshold, NumTest)
    
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
            cmbVector = joint(train_data[:, np.array(list(col))])
            datasizeFlag = checkDataSize(train_data[:, x], targets, cmbVector)
            if datasizeFlag != 1:
                NumTest = NumTest + 1
                T = cmi(train_data[:, x], targets, cmbVector, 0)
                if T > threshold:                    # v structure             
                    temp = set(PCD).union(set([x]))
                    for s in np.setdiff1d(np.array(list(temp)), y): 
                        T = cmi(train_data[:, y], targets, train_data[:, s], 0)
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
        if spouse[y] != []:
           S.append( y)    # Y has spouses
           # shrink
           spousecan = spouse[y]
           for sind in np.arange(spousecan.size):
               s = spousecan[sind]
               col = set([y]).union(set(spousecan),set(PCD))
               cmbVector = joint(train_data[:, np.setdiff1d(np.array(list(col)), s)])
               datasizeFlag = checkDataSize(train_data[:, s], targets, cmbVector)
               if datasizeFlag != 1:
                  NumTest = NumTest + 1
                  T = cmi(train_data[:, s], targets, cmbVector, 0)
                  if T < threshold:
                     NonS = set(NonS).union(set([s]))
           spouse[y] = np.setdiff1d(spousecan, np.array(list(NonS)))
           NonS = []
                                                            
    b = [];
    for i in np.arange(len(spouse)):
         if spouse[i] != []:
             b = set(b).union(set(spouse[i]))
    # remove false spouse from PC
    M = PCD       # setdiff(PCD,S); % M has no spouses in PCD set
    PCsize = M.size
    testSet = set(S).union(set(b))
    #testSet = np.array(list(temp))
    C = np.zeros(shape = (PCsize, 1))
    for x in M:
       col = set(PCD).union(set(testSet))
       temp = np.setdiff1d(np.array(list(col)), x)
       cmbVector = joint(train_data[:, temp])
       datasizeFlag = checkDataSize(train_data[:, x], targets, cmbVector)
       if datasizeFlag != 1:
            NumTest = NumTest + 1
            T = cmi(train_data[:, x], targets, cmbVector, 0)
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