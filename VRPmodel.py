# Imports
import math
import random

class Node:
    def __init__(self, id, tp, dem, xx, yy):
        self.id = id
        self.type = tp
        self.demand = dem
        self.x = xx
        self.y = yy
        self.isRouted = False

    def __repr__(self):  
        return "%s %s %s %s %s" % (self.id, self.type, self.demand, self.x, self.y)

class Model:
    # instance variables
    def __init__(self):
        self.allNodes = []
        self.service_locations = []
        self.dist_matrix = []
        self.time_matrix = []

    def createNodes(self):
        depot = Node(0, 0, 0, 50, 50)
        self.allNodes.append(depot)
        random.seed(1)

        for i in range(0,200):
            id = i + 1
            tp = random.randint(1, 3)
            dem = random.randint(1, 5) * 100
            xx = random.randint(0, 100)
            yy = random.randint(0, 100)
            serv_node = Node(id, tp, dem, xx, yy)
            self.allNodes.append(serv_node)
            self.service_locations.append(serv_node)

    # Sort service locations based on demand
    def sortNodes(self):
        self.service_locations.sort(key = lambda x: x.demand, reverse=True)

    def createDistanceMatrix(self):
        self.dist_matrix = [[0.0 for j in range(0, len(self.allNodes))] for k in range(0, len(self.allNodes))]

        for i in range(0, len(self.allNodes)):
            for j in range(0, len(self.allNodes)):
                source = self.allNodes[i]
                target = self.allNodes[j]
                dx_2 = (source.x - target.x) ** 2
                dy_2 = (source.y - target.y) ** 2
                dist = round(math.sqrt(dx_2 + dy_2))
                self.dist_matrix[i][j] = dist

    def createTimeMatrix(self):
        speed = 35 # Truck speed (km/h)
        type = {0:0, 1:5, 2:15, 3:25} # Service locations' type based on unloading time (mins)
        self.time_matrix = [[0.0 for j in range(0, len(self.allNodes))] for k in range(0, len(self.allNodes))]

        for i in range(0, len(self.allNodes)):
            for j in range(0, len(self.allNodes)):
                # Convert km to hours using speed
                self.time_matrix[i][j] = self.dist_matrix[i][j]/speed
                # Add unloading time of destination in hours
                target = self.allNodes[j]
                self.time_matrix[i][j] += type[target.type]/60

class Solution:
    def __init__(self):
        self.trucks = []
        self.max_travel_time = 0
        self.last_truck_id = 0

    def CalculateMaxTravelTime(self,m):
        self.max_travel_time = 0
        self.last_truck_id = 0
        for i in range(0,len(self.trucks)):
            truck = self.trucks[i]
            truck.CalculateTravelTime(m)
            if truck.travel_time > self.max_travel_time:
                self.max_travel_time = truck.travel_time
                self.last_truck_id = i

    def AddTruck(self):
        newTruck = Truck()
        newTruck.kgOnTruck = 0
        self.trucks.append(newTruck)

    def ReportSolution(self):
        print("Number of trucks: ",len(self.trucks))
        print("Max travel time: ",self.max_travel_time)
        print("Longest route: ")
        self.trucks[self.last_truck_id].ShowRoute()
        print("\n")
        print("Solution routes: ")
        for truck in self.trucks:
            truck.ShowRoute()
            print("\n",truck.travel_time)
            print(truck.kgOnTruck,"\n")

class Truck:
    def __init__(self):
        self.emptySpace = 3000
        self.kgOnTruck = 0
        self.nodesOnRoute = []
        self.travel_time = 0

    def CalculateTravelTime(self,m):
        self.travel_time = 0
        truckNodes = self.nodesOnRoute
        for i in range(0, len(truckNodes)-1):
            self.travel_time += m.time_matrix[truckNodes[i].id][truckNodes[i+1].id]

    def AddNode(self,toBeAssigned):
        self.nodesOnRoute.append(toBeAssigned)
        self.kgOnTruck = self.kgOnTruck + toBeAssigned.demand
        self.emptySpace = self.emptySpace - toBeAssigned.demand

    def ShowRoute(self):
        for i in range (0, len(self.nodesOnRoute)):
            print(self.nodesOnRoute[i].id, end = ' ')