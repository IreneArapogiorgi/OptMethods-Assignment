# Imports
import math
import random
import VRPmodel as v
import BinPackingAlgorithms as b
import TSP as t
import improvement as im

# Constants
Q = 3000 # Maximum truck load (kg)
T = 25 # Maximum number of trucks

def main():
    m = v.Model()
    m.createNodes()
    m.createDistanceMatrix()
    m.createTimeMatrix()
    m.sortNodes()
    sol = v.Solution()

    print("******Bin Packing******")
    b.BestFit(sol, m.allNodes)
    sol.CalculateMaxTravelTime(m)
    sol.ReportSolution()

    print("******TSP Improvement******")
    for i in range(0, len(sol.trucks)):
        sol.trucks[i] = t.MinimumInsertions(sol.trucks[i], m.time_matrix)
    sol.CalculateMaxTravelTime(m)
    sol.ReportSolution()
    
    print("******Improved Fleet Utilization******")
    if len(sol.trucks) < 25 :
        im.improveFleetUtilization(sol, m)
    sol.CalculateMaxTravelTime(m)
    sol.ReportSolution()

main()
