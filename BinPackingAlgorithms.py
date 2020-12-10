# Imports
import math
import random
import VRPmodel

# Best-Fit Algorithm
def BestFit(sol, all_nodes):

    totalNodes = len(all_nodes)
    depot = all_nodes[0]
    for i in range(1, totalNodes):

        toBeAssigned = all_nodes[i]
        indexOfBestTruck = -1
        minimumEmptySpace = 1000000

        totalOpenTrucks = len(sol.trucks)

        for b in range(0, totalOpenTrucks):
            trialTruck = sol.trucks[b]
            if (trialTruck.emptySpace >= toBeAssigned.demand):
                if (trialTruck.emptySpace < minimumEmptySpace):
                    minimumEmptySpace = trialTruck.emptySpace
                    indexOfBestTruck = b

        if (indexOfBestTruck != -1):
            truckOfInsertion: Truck = sol.trucks[indexOfBestTruck]
            truckOfInsertion.AddNode(toBeAssigned)
        else:
            sol.AddTruck()
            truckOfInsertion=sol.trucks[len(sol.trucks)-1]
            truckOfInsertion.AddNode(depot)
            truckOfInsertion.AddNode(toBeAssigned)