import VRPmodel as v

def SetRoutedFlagToFalseForAllCustomers(customers):
    for i in range (1, len(customers)):
        customers[i].isRouted = False

"""
def ApplyNearestNeighborMethod(depot, customers, sol, distanceMatrix):
    sol.sequenceOfNodes.append(depot)
    for i in range (0, len(customers)):
        indexOfTheNextCustomer = -1
        minimumInsertionCost = 1000000
        lastIndexInSolution = len(sol.sequenceOfNodes) - 1
        lastNodeInTheCurrentSequence = sol.sequenceOfNodes[lastIndexInSolution]

        for j in range (0, len(customers)):
            candidate = customers[j]
            if candidate.isRouted == True:
                continue
            trialCost = distanceMatrix[lastNodeInTheCurrentSequence.ID][candidate.ID]
            if (trialCost < minimumInsertionCost):
                indexOfTheNextCustomer = j
                minimumInsertionCost = trialCost

        insertedCustomer = customers[indexOfTheNextCustomer]
        sol.sequenceOfNodes.append(insertedCustomer)
        sol.cost += distanceMatrix[lastNodeInTheCurrentSequence.ID][insertedCustomer.ID]
        insertedCustomer.isRouted = True

    lastIndexInSolution = len(sol.sequenceOfNodes) - 1
    lastNodeInTheCurrentSequence = sol.sequenceOfNodes[lastIndexInSolution]
    sol.sequenceOfNodes.append(depot)
    sol.cost += distanceMatrix[lastNodeInTheCurrentSequence.ID][depot.ID]
"""
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

        insertedCustomer = allNodes[indexOfTheNextCustomer]
        newTruck.nodesOnRoute.insert(positionOfInsertion, insertedCustomer)
        newTruck.travel_time += minimumInsertionCost
        insertedCustomer.isRouted = True
    return newTruck
    '''for i in range (0, len(truck.nodesOnRoute)):
            print(truck.nodesOnRoute[i].id, end = ' ')
    print("\n",truck.travel_time,"\n")
    '''

"""
def CheckSolution(sol, distanceMatrix):
    cst = 0
    for i in range(len(sol.sequenceOfNodes) - 1):
        a = sol.sequenceOfNodes[i]
        b = sol.sequenceOfNodes[i+1]
        cst += distanceMatrix[a.ID][b.ID]
    if (abs(cst - sol.cost) > 0.00001):
        print('Error')


def solve(m):

    allNodes = m.allNodes
    customers = m.customers
    depot = allNodes[0]
    distanceMatrix = m.matrix

    sol1 = Solution()
    #sol2 = Solution()

    SetRoutedFlagToFalseForAllCustomers(customers)
    #ApplyNearestNeighborMethod(depot, customers, sol1, distanceMatrix)
    MinimumInsertions(depot, customers, sol1, distanceMatrix)
    CheckSolution(sol1, distanceMatrix)
    #CheckSolution(sol2, distanceMatrix)
    ReportSolution(sol1)
    #ReportSolution(sol2)    

#m = Model()
#m.BuildModel()
#solve(m)
"""




