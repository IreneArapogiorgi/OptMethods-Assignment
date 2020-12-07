# Imports
import math
import random

# Nodes' Creation
class Node:
    def __init__(self, id, tp, dem, xx, yy):
        self.id = id
        self.type = tp
        self.demand = dem
        self.x = xx
        self.y = yy

# Solution Creation
class Solution:
    def __init__(self):
        self.trucks = []

# Truck Creation
class Truck:
    def __init__(self):
        self.emptySpace = 0
        self.kgOnTruck = 0
        self.nodesOnRoute = []

# Sort service locations based on demand
def sortNodes(listOFNodes: list):
    listOFNodes.sort(key = lambda x: x.demand, reverse=True)

# Best-Fit Algorithm
def BestFit(sol, all_nodes, Q):

    totalNodes = len(all_nodes)

    for i in range(0, totalNodes):

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
            truckOfInsertion.nodesOnRoute.append(toBeAssigned)
            truckOfInsertion.kgOnTruck = truckOfInsertion.kgOnTruck + toBeAssigned.demand
            truckOfInsertion.emptySpace = truckOfInsertion.emptySpace - toBeAssigned.demand
        else:
            newTruck = Truck()
            newTruck.kgOnTruck = 0
            newTruck.emptySpace = Q

            sol.trucks.append(newTruck)
            newTruck.nodesOnRoute.append(toBeAssigned)
            newTruck.kgOnTruck = newTruck.kgOnTruck + toBeAssigned.demand
            newTruck.emptySpace = newTruck.emptySpace - toBeAssigned.demand

# Main Method
def main():
    # Constants
    Q = 3000 # Maximum truck load - capacity (kg)
    speed = 35 # Truck speed (km/h)
    type = {0:0, 1:5, 2:15, 3:25} # Service locations' type based on unloading time (mins)

    # Initialize nodes - service locations
    all_nodes = []
    service_locations = []
    depot = Node(0, 0, 0, 50, 50)
    all_nodes.append(depot)
    random.seed(1)

    for i in range(0, 200):
        id = i + 1
        tp = random.randint(1, 3)
        dem = random.randint(1, 5) * 100
        xx = random.randint(0, 100)
        yy = random.randint(0, 100)
        serv_node = Node(id, tp, dem, xx, yy)
        all_nodes.append(serv_node)
        service_locations.append(serv_node)

    # Create solution
    sol = Solution()

    # Sort nodes - service locations
    sortNodes(all_nodes)

    # Run best-fit algorithm
    BestFit(sol, all_nodes, Q)

    # Print number of trucks needed
    print(len(sol.trucks))

    # Create distance matrix
    dist_matrix = [[0.0 for j in range(0, len(all_nodes))] for k in range(0, len(all_nodes))]

    for i in range(0, len(all_nodes)):
        for j in range(0, len(all_nodes)):
            source = all_nodes[i]
            target = all_nodes[j]
            dx_2 = (source.x - target.x) ** 2
            dy_2 = (source.y - target.y) ** 2
            dist = round(math.sqrt(dx_2 + dy_2))
            dist_matrix[i][j] = dist

    # Create time matrix
    time_matrix = [[0.0 for j in range(0, len(all_nodes))] for k in range(0, len(all_nodes))]

    for i in range(0, len(all_nodes)):
        for j in range(0, len(all_nodes)):
            # Convert km to hours using speed
            time_matrix[i][j] = dist_matrix[i][j]/speed
            # Add unloading time of destination in hours
            target = all_nodes[j]
            time_matrix[i][j] += type[target.type]/60

    # Calculate maximum travel time
    max_travel_time = 0

    for truck in sol.trucks:
        travel_time = 0
        # Nodes of each truck
        truckNodes = truck.nodesOnRoute
        for i in range(0, len(truckNodes)-1):
            travel_time += time_matrix[truckNodes[i].id][truckNodes[i+1].id]

        if travel_time > max_travel_time:
            max_travel_time = travel_time
    
    # Print maximum travel time
    print(max_travel_time)

main()