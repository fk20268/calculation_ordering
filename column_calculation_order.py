from __future__ import print_function
import json

calcsA = json.load(open('col_calcs_A.json'))
calcsB = json.load(open('col_calcs_B.json'))
calcsC = json.load(open('col_calcs_C.json'))

def check_order_holds(columnDependencyDict,keyOrdering):
    for currentCalcKey in keyOrdering:
        for otherCalcKey in keyOrdering:
            # if the other calculation depends on this calculation AND the index of the other calculation is larger => incorrect order 
            if (currentCalcKey in columnDependencyDict[otherCalcKey]) and (keyOrdering.index(currentCalcKey)> keyOrdering.index(otherCalcKey)):
                """  # swapping the two erroneous indexes so the old and new ordering of keys is different -> triggers re-sort
                temp = keyOrdering[keyOrdering.index(currentCalcKey)]
                keyOrdering[keyOrdering.index(currentCalcKey)] = keyOrdering[keyOrdering.index(otherCalcKey)]
                keyOrdering[keyOrdering.index(otherCalcKey)] = temp
                print("reordered " + str(keyOrdering))"""
                index1 = keyOrdering.index(currentCalcKey)
                index2 = index1 - 1
                temp = keyOrdering[index1]
                keyOrdering[index1] = keyOrdering[index2]
                keyOrdering[index2] = temp
                print("WHAT + " + str(keyOrdering) )
    return keyOrdering

#recursive function that checks if the key order has been changed since the last iteration. If it hasnt => sorted. otherwise recall
def order_column_calculations(calculationList, columnDependencyDict, origKeyOrdering):
    newKeyOrdering = []
    for currentCalcKey in origKeyOrdering:
        # if no backticks it can just be appended to the front as it relies on no other column
        if "`" not in calculationList[currentCalcKey]:
            newKeyOrdering.insert(0,currentCalcKey)
        else: 
            for columnDependency in columnDependencyDict[currentCalcKey]:
                if (currentCalcKey in newKeyOrdering) and (columnDependency in newKeyOrdering):
                    if newKeyOrdering.index(currentCalcKey) > newKeyOrdering.index(columnDependency):
                        newKeyOrdering.remove(columnDependency)
                        newKeyOrdering.insert(newKeyOrdering.index(currentCalcKey),columnDependency)
                elif (currentCalcKey in newKeyOrdering) and (columnDependency not in newKeyOrdering):
                    newKeyOrdering.insert(newKeyOrdering.index(currentCalcKey),columnDependency)
                else: 
                    newKeyOrdering.insert(len(newKeyOrdering),currentCalcKey)
        # if nothing depends on the column it wont have been added yet, so just append it to the end of the ordering (N.B. it can still depend on other columns)
        if currentCalcKey not in newKeyOrdering:
            newKeyOrdering.insert(len(newKeyOrdering),currentCalcKey)
    # iterate through the ordering to see if its correct. if it isnt swap the two items that cause it to be out of order and trigger a re-sort
    newKeyOrdering = check_order_holds(columnDependencyDict, newKeyOrdering)
    if (newKeyOrdering == origKeyOrdering):
        return newKeyOrdering
    else:
        return order_column_calculations(calculationList, columnDependencyDict, newKeyOrdering)
    
#a function to create a clean dictionary where the value for each column is a list of the other columns it depends on
def calc_column_dependencies(calculationList):
    newKeyOrdering = []
    columnDependencyDict = {}
    
    for currentCalcKey in calculationList:
        newKeyOrdering.append(currentCalcKey)
        refList = []
        for otherCalcKey in calculationList: 
            if (otherCalcKey in calculationList[currentCalcKey]) and (currentCalcKey != otherCalcKey): 
                #the line below checks if there is a trailing backtick (i.e. is the ENTIRE column name present?)
                if calculationList[currentCalcKey][calculationList[currentCalcKey].index(otherCalcKey)+ len(currentCalcKey)] =='`':
                    refList.append(otherCalcKey)
                    columnDependencyDict[currentCalcKey] = refList            
        if currentCalcKey not in columnDependencyDict:
            columnDependencyDict[currentCalcKey] = ""
    print(columnDependencyDict)
    newKeyOrdering = order_column_calculations(calculationList, columnDependencyDict, list(calculationList.keys()))
    return newKeyOrdering    
    
    
#thefunction to call in order to sort thje
def key_ordering(calculationList):
    calcKeyOrdering = list(calculationList.keys())
    newKeyOrdering = calc_column_dependencies(calculationList)
    return newKeyOrdering  



newOrderingCalcsA = key_ordering(calcsA)
newOrderingCalcsB = key_ordering(calcsB)


print(list(calcsA.keys()))
print("\n NEW ORDERING BELOW \n")
newOrderingCalcsA = key_ordering(calcsA)
print(newOrderingCalcsA)

print(list(calcsB.keys()))
print("\n NEW ORDERING BELOW \n")
newOrderingCalcsB = key_ordering(calcsB)
print(newOrderingCalcsB)

print(list(calcsC.keys()))
print("\n NEW ORDERING BELOW \n")
newOrderingCalcsC = key_ordering(calcsC)
print("FINAL :  " + str(newOrderingCalcsC))


