# Imports
from TSPmodel import Model
from SolutionDrawer import *

class Solution:
    def __init__(self):
        self.cost = 0.0
        self.routes = []
        self.truckload = 3000 # Maximum truck load

def SetRoutedFlagToFalseForAllCustomers(service_locations):
    for i in range (0, len(service_locations)):
        service_locations[i].isRouted = False

def MinimumInsertions(depot, service_locations, sol, time_matrix):
    sol.cost = 0 # Initialize each route's cost
    sequenceOfNodes = []
    sequenceOfNodes.append(depot)
    sequenceOfNodes.append(depot)
    demand = depot.demand

    for i in range (0, len(service_locations)):
        indexOfTheNextCustomer = -1
        positionOfInsertion = -1
        minimumInsertionCost = 100000000000

        for j in range(0, len(service_locations)):
            candidate = service_locations[j]
            if candidate.isRouted == True:
                continue
            if (demand + candidate.demand) > sol.truckload:
                continue
            for k in range(0, len(sequenceOfNodes) - 1):
                before = sequenceOfNodes[k]
                after = sequenceOfNodes[k + 1]
                costAdded = time_matrix[before.id][candidate.id] + time_matrix[candidate.id][after.id]
                costRemoved = time_matrix[before.id][after.id]
                trialCost = costAdded - costRemoved
                if trialCost < minimumInsertionCost:
                    indexOfTheNextCustomer = j
                    positionOfInsertion = k
                    minimumInsertionCost = trialCost

        insertedCustomer = service_locations[indexOfTheNextCustomer]
        sequenceOfNodes.insert(positionOfInsertion + 1, insertedCustomer)
        sol.cost += minimumInsertionCost
        demand += insertedCustomer.demand
        insertedCustomer.isRouted = True

        if demand == sol.truckload:
            sol.routes.append(sequenceOfNodes)
            break

def ReportSolution(sol, totalCost):
    for route in sol.routes:
        for i in range(0, len(route)):
            print(route[i].id, end = ' ')
        print()
    print("Total cost is: ", totalCost)

def solve(m):
    allNodes = m.allNodes
    service_locations = m.service_locations
    depot = allNodes[0]
    time_matrix = m.time_matrix

    sol = Solution()
    totalCost = sol.cost

    SetRoutedFlagToFalseForAllCustomers(service_locations) # maybe not needed because flag is false by default

    for i in range(0, 26):
        depot.isRouted = False
        MinimumInsertions(depot, service_locations, sol, time_matrix)
        totalCost += sol.cost
        #SolDrawer.draw(i, sol, allNodes)

    # Report routes and cost
    ReportSolution(sol, totalCost)

def main():
    m = Model()
    m.createNodes()
    m.createDistanceMatrix()
    m.createTimeMatrix()
    m.sortNodes()
    solve(m)

main()