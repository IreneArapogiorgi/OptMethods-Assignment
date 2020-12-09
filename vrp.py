# Imports
import math
import random
import VRPmodel as v
import BinPackingAlgorithms as b

# Constants
Q = 3000 # Maximum truck load (kg)
T = 26 # Maximum number of trucks

def main():
    m = v.Model()
    m.createNodes()
    m.createDistanceMatrix()
    m.createTimeMatrix()
    m.sortNodes()
    sol = v.Solution()
    b.BestFit(sol,m.allNodes,Q)
    sol.CalculateMaxTravelTime(m)
    print(len(sol.trucks))
    print(sol.max_travel_time)
main()