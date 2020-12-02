# Imports
import math
import random

# Constants
Q = 3000 # Maximum truck load (kg)
speed = 35 # Truck speed (km/h)
type = {0:0, 1:5, 2:15, 3:25} # Service locations' type based on unloading time (mins)

# Nodes' Creation
class Node:
    def __init__(self, id, tp, dem, xx, yy):
        self.id = id
        self.type = tp
        self.demand = dem
        self.x = xx
        self.y = yy

    def __repr__(self):  
        return "%s %s %s %s %s" % (self.id, self.type, self.demand, self.x, self.y)

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
    # Convert km to hours using speed
    time_matrix[i] = [x/speed for x in dist_matrix[i]]
    for j in range(0, len(all_nodes)):
        target = all_nodes[j]
        # Add unloading time of destination in hours
        time_matrix[i][j] += type[target.type]/60

# Initialize each truck's route
routes = {truck:[] for truck in range(1, 26)}