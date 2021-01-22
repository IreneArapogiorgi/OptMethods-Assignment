# Imports
import VRPmodel as v
import BinPackingAlgorithm as b
import TSP as t
import improvement as im
from VND import *
from Solver import *
import timeit

start_time = timeit.default_timer()

# Constants
T = 25 # Maximum number of trucks

def cloneRoute(rt:Truck):
    cloned = Truck()
    cloned.travel_time = rt.travel_time
    cloned.kgOnTruck = rt.kgOnTruck
    cloned.nodesOnRoute = rt.nodesOnRoute.copy()
    return cloned

def cloneSolution(sol: Solution):
    cloned = Solution()
    for i in range (0, len(sol.trucks)):
        rt = sol.trucks[i]
        clonedRoute = cloneRoute(rt)
        cloned.trucks.append(clonedRoute)
    cloned.max_travel_time = sol.max_travel_time
    return cloned

def extractSolution(sol):
    with open("sol_t8160012.txt","w") as file:
        file.write(str(sol.max_travel_time)+"\n")
        for truck in sol.trucks:
            nodes_list = [str(node.id) for node in truck.nodesOnRoute]
            file.write(",".join(nodes_list))
            file.write("\n")

def main():
    m = v.Model()
    m.createNodes()
    m.createDistanceMatrix()
    m.createTimeMatrix()
    m.sortNodes()
    sol = v.Solution()

    print()
    #print("******Solution******")
    b.BestFitTime(sol, m.allNodes, m.time_matrix)
    sol.CalculateMaxTravelTime(m)
    #sol.ReportSolution()

    #print("******TSP Improvement******")
    for i in range(0, len(sol.trucks)):
        if len(sol.trucks[i].nodesOnRoute)< 2:
            continue
        sol.trucks[i] = t.MinimumInsertions(sol.trucks[i], m.time_matrix)
    sol.CalculateMaxTravelTime(m)
    #sol.ReportSolution()
    
    #print("******Improved Fleet Utilization******")
    im.improveFleetUtilization(sol, m)
    sol.CalculateMaxTravelTime(m)
    #sol.ReportSolution()

    bestSol = sol

    while timeit.default_timer() - start_time <= 300.0:

        #print("******VND classic******")
        solv = Solver2(m,sol)
        sol = solv.solve(start_time)
        sol.CalculateMaxTravelTime(m)
        #sol.ReportSolution()

        if sol.max_travel_time < bestSol.max_travel_time:
            bestSol = cloneSolution(sol)
            
        #print("******VND modified******")
        solv = Solver(m,sol)
        sol = solv.solve(start_time)
        sol.CalculateMaxTravelTime(m)
        #sol.ReportSolution()

        if sol.max_travel_time < bestSol.max_travel_time:
            bestSol = cloneSolution(sol)
            
    #print("******Best Solution******")
    bestSol.ReportSolution()
    extractSolution(sol)

    print(timeit.default_timer() - start_time)

main()