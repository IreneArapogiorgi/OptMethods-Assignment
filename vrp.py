# Imports
import VRPmodel as v
import BinPackingAlgorithm as b

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

main()