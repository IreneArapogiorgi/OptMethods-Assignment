import VRPmodel as v

def SetRoutedFlagToFalseForAllCustomers(customers):
    customers[0].isRouted = False
    for i in range (1, len(customers)):
        customers[i].isRouted = False

def MinimumInsertions(truck, timeMatrix):
    allNodes = truck.nodesOnRoute
    SetRoutedFlagToFalseForAllCustomers(allNodes)
    newTruck = v.Truck()
    newTruck.nodesOnRoute.append(allNodes[0])

    #add first node
    indexOfTheNextCustomer = -1
    minimumInsertionCost = 1000000
    for p in range(1,len(allNodes)):
            trialCost = timeMatrix[0][allNodes[p].id]
            if trialCost < minimumInsertionCost:
                    indexOfTheNextCustomer = p
                    minimumInsertionCost = trialCost
    insertedCustomer = allNodes[indexOfTheNextCustomer]
    newTruck.nodesOnRoute.insert(1, insertedCustomer)
    newTruck.travel_time += minimumInsertionCost
    newTruck.kgOnTruck += insertedCustomer.demand
    newTruck.emptySpace -= insertedCustomer.demand
    insertedCustomer.isRouted = True

    for i in range (2, len(allNodes)):
        indexOfTheNextCustomer = -1
        positionOfInsertion = -1
        minimumInsertionCost = 1000000
        for j in range(1, len(allNodes)):
            candidate = allNodes[j]
            if candidate.isRouted == True:
                continue
            for k in range(1, len(newTruck.nodesOnRoute)):
                before = newTruck.nodesOnRoute[k-1]
                after = newTruck.nodesOnRoute[k]
                costAdded = timeMatrix[before.id][candidate.id] + timeMatrix[candidate.id][after.id]
                costRemoved = timeMatrix[before.id][after.id]
                trialCost = costAdded - costRemoved
                if trialCost < minimumInsertionCost:
                    indexOfTheNextCustomer = j
                    positionOfInsertion = k
                    minimumInsertionCost = trialCost
            if timeMatrix[newTruck.nodesOnRoute[len(newTruck.nodesOnRoute)-1].id][candidate.id]< minimumInsertionCost:
                indexOfTheNextCustomer = j
                positionOfInsertion = len(newTruck.nodesOnRoute)
                minimumInsertionCost = timeMatrix[newTruck.nodesOnRoute[len(newTruck.nodesOnRoute)-1].id][candidate.id]
        insertedCustomer = allNodes[indexOfTheNextCustomer]
        newTruck.nodesOnRoute.insert(positionOfInsertion, insertedCustomer)
        newTruck.travel_time += minimumInsertionCost
        newTruck.kgOnTruck += insertedCustomer.demand
        newTruck.emptySpace -= insertedCustomer.demand
        insertedCustomer.isRouted = True
    return newTruck