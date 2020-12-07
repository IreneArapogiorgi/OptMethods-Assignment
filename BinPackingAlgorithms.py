import random
import math

# Nodes' Creation
class Node:
    def __init__(self, id, tp, dem, xx, yy):
        self.id = id
        self.type = tp
        self.demand = dem
        self.x = xx
        self.y = yy

class Solution:
    def __init__(self):
        self.trucks = []

class Truck:
    def __init__(self):
        self.emptySpace = 0
        self.kgOnTruck = 0
        self.nodesOnRoute = []

def main():
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

    speed = 35
    type = {0:0, 1:5, 2:15, 3:25} # Service locations' type based on unloading time (mins)
    Q = 3000 #truck capacity
    sol = Solution()

    sortNodes(all_nodes)

    BestFit(sol, all_nodes, Q)
    print(len(sol.trucks))
    # Distance Matrix Creation
    dist_matrix = [[0.0 for j in range(0, len(all_nodes))] for k in range(0, len(all_nodes))]

    for i in range(0, len(all_nodes)):
        for j in range(0, len(all_nodes)):
            source = all_nodes[i]
            target = all_nodes[j]
            dx_2 = (source.x - target.x) ** 2
            dy_2 = (source.y - target.y) ** 2
            dist = round(math.sqrt(dx_2 + dy_2))
            dist_matrix[i][j] = dist

    # Time Matrix Creation
    time_matrix = [[0.0 for j in range(0, len(all_nodes))] for k in range(0, len(all_nodes))]

    for i in range(0, len(all_nodes)):
        for j in range(0, len(all_nodes)):
            # Convert km to hours using speed
            time_matrix[i][j] = dist_matrix[i][j]/speed
            target = all_nodes[j]
            # Add unloading time of destination in hours
            time_matrix[i][j] += type[target.type]/60

    sol.trucks.clear()

    max_travel_time = 0
    for truck in sol.trucks:
        travel_time = 0
        for i in range(0,len(truck)-1):
            travel_time+=time_matrix[truck[i]][truck[i+1]]
        if travel_time > max_travel_time :
            max_travel_time = travel_time
    print(max_travel_time)

def sortNodes(listOFNodes: list):
    listOFNodes.sort(key = lambda x: x.demand, reverse=True)

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

main()