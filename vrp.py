# Imports
import VRPmodel as v
import BinPackingAlgorithm as b
import TSP as t
import improvement as im
from VND import *
from Solver import *

# Constants
T = 25 # Maximum number of trucks

def main():
    m = v.Model()
    m.createNodes()
    m.createDistanceMatrix()
    m.createTimeMatrix()
    m.sortNodes()
    sol = v.Solution()

    print()
    print("******Solution******")
    b.BestFitTime(sol, m.allNodes, m.time_matrix)
    sol.CalculateMaxTravelTime(m)
    sol.ReportSolution()

    print("******TSP Improvement******")
    for i in range(0, len(sol.trucks)):
        sol.trucks[i] = t.MinimumInsertions(sol.trucks[i], m.time_matrix)
    sol.CalculateMaxTravelTime(m)
    sol.ReportSolution()
    
    print("******Improved Fleet Utilization******")
    im.improveFleetUtilization(sol, m)
    sol.CalculateMaxTravelTime(m)
    sol.ReportSolution()

    print("******VND******")
    solv = Solver2(m,sol)
    sol = solv.solve()
    sol.CalculateMaxTravelTime(m)
    sol.ReportSolution()

    print("******VND******")
    solv = Solver(m,sol)
    sol = solv.solve()
    sol.CalculateMaxTravelTime(m)
    sol.ReportSolution()

main()