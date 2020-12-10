# Imports
import math
import random
import VRPmodel as v
import BinPackingAlgorithms as b
#import TSP as t

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
    b.BestFit(sol,m.allNodes)
    sol.CalculateMaxTravelTime(m)
    print("******Bin Packing******")
    sol.ReportSolution()
    #for truck in sol.trucks:
    #    t.MinimumInsertions(truck)
main()