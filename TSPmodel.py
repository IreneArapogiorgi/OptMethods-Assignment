# Imports
import random
import math

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
    # Instance variables
    def __init__(self):
        self.nodesNum = 200
        self.allNodes = []
        self.service_locations = []
        self.dist_matrix = []
        self.time_matrix = []

    # Create nodes
    def createNodes(self):
        depot = Node(0, 0, 0, 50, 50)
        self.allNodes.append(depot)
        random.seed(1)

        for i in range(0, self.nodesNum):
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

    # Create distance matrix
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

    # Create time matrix
    def createTimeMatrix(self):
        speed = 35 # Truck speed (km/h)
        type = {0:0, 1:5, 2:15, 3:25} # Service locations' type based on unloading time (mins)
        self.time_matrix = [[0.0 for j in range(0, len(self.allNodes))] for k in range(0, len(self.allNodes))]

        for i in range(0, len(self.allNodes)):
            for j in range(0, len(self.allNodes)):
                target = self.allNodes[j]
                # Convert km to hours using speed & add unloading time of destination in hours
                self.time_matrix[i][j] = self.dist_matrix[i][j]/speed + type[target.type]/60