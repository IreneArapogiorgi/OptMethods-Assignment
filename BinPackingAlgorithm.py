# Imports
import VRPmodel

# Best-fit algorithm altered to fit nodes based on cost and fill up trucks based on their load
def BestFitTime(sol, all_nodes, timeMatrix):
    totalNodes = len(all_nodes)
    depot = all_nodes[0]

    for i in range(1, totalNodes):
        toBeAssigned = all_nodes[i]
        indexOfBestTruck = -1
        minimumCost = 1000000

        totalOpenTrucks = len(sol.trucks)

        for b in range(0, totalOpenTrucks):
            trialTruck = sol.trucks[b]
            if (trialTruck.emptySpace >= toBeAssigned.demand):
                lastNode = trialTruck.nodesOnRoute[-1]
                toBeAddedCost = timeMatrix[lastNode.id][toBeAssigned.id]

                if (toBeAddedCost < minimumCost):
                    minimumCost = toBeAddedCost
                    indexOfBestTruck = b

        if (indexOfBestTruck != -1):
            truckOfInsertion: Truck = sol.trucks[indexOfBestTruck]
            truckOfInsertion.AddNode(toBeAssigned)
        else:
            sol.AddTruck()
            truckOfInsertion = sol.trucks[len(sol.trucks)-1]
            truckOfInsertion.AddNode(depot)
            truckOfInsertion.AddNode(toBeAssigned)

        # Do not add an new truck, if there's already an empty one
        if (len(sol.trucks[-1].nodesOnRoute) == 1):
            continue

        # Add a new truck
        sol.AddTruck()
        truck = sol.trucks[-1]
        truck.AddNode(depot)