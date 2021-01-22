from VRPmodel import *
from SolutionDrawer import *

class RelocationMove(object):
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = None

    def Initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = 10 ** 9


class SwapMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = None

    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = 10 ** 9


class CustomerInsertion(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.cost = 10 ** 9


class CustomerInsertionAllPositions(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.insertionPosition = None
        self.cost = 10 ** 9


class TwoOptMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = None

    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = 10 ** 9


class Solver2:
    def __init__(self, m, sol):
        self.allNodes = m.allNodes
        self.service_locations = m.service_locations
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.time_matrix
        self.capacity = 3000
        self.sol = sol
        self.model = m
        self.bestSolution = None
        self.searchTrajectory = []

    def solve(self):
        #self.SetRoutedFlagToFalseForAllCustomers()
        #self.ApplyNearestNeighborMethod()
        #self.MinimumInsertions()
        #self.ReportSolution(self.sol)
        #self.LocalSearch(2)
        self.VND()
        self.ReportSolution(self.sol)
        return self.sol

    def SetRoutedFlagToFalseForAllCustomers(self):
        for i in range(0, len(self.service_locations)):
            self.service_locations[i].isRouted = False

    def ApplyNearestNeighborMethod(self):
        modelIsFeasible = True
        self.sol = Solution()
        insertions = 0

        while (insertions < len(self.service_locations)):
            bestInsertion = CustomerInsertion()
            lastOpenRoute: Truck = self.GetLastOpenRoute()

            if lastOpenRoute is not None:
                self.IdentifyBestInsertion(bestInsertion, lastOpenRoute)

            if (bestInsertion.customer is not None):
                self.ApplyCustomerInsertion(bestInsertion)
                insertions += 1
            else:
                #If there is an empty available route
                if lastOpenRoute is not None and len(lastOpenRoute.nodesOnRoute) == 2:
                    modelIsFeasible = False
                    break
                else:
                    self.sol.AddTruck()
                    truckOfInsertion = sol.trucks[len(sol.trucks)-1]
                    truckOfInsertion.AddNode(self.depot)
        
        if (modelIsFeasible == False):
            print('FeasibilityIssue')
            #reportSolution

    def MinimumInsertions(self):
        modelIsFeasible = True
        self.sol = Solution()
        insertions = 0

        while (insertions < len(self.service_locations)):
            bestInsertion = CustomerInsertionAllPositions()
            lastOpenRoute: Truck = self.GetLastOpenRoute()

            if lastOpenRoute is not None:
                self.IdentifyBestInsertionAllPositions(bestInsertion, lastOpenRoute)

            if (bestInsertion.customer is not None):
                self.ApplyCustomerInsertionAllPositions(bestInsertion)
                insertions += 1
            else:
                # If there is an empty available route
                if lastOpenRoute is not None and len(lastOpenRoute.nodesOnRoute) == 2:
                    modelIsFeasible = False
                    break
                # If there is no empty available route and no feasible insertion was identified
                else:
                    self.sol.AddTruck()
                    truckOfInsertion = sol.trucks[len(sol.trucks)-1]
                    truckOfInsertion.AddNode(self.depot)

        if (modelIsFeasible == False):
            print('FeasibilityIssue')
            # reportSolution

        self.TestSolution()

    def LocalSearch(self, operator):
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        localSearchIterator = 0

        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()

        while terminationCondition is False:

            self.InitializeOperators(rm, sm, top)
            SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)

            # Relocations
            if operator == 0:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None:
                    if rm.moveCost < 0:
                        self.ApplyRelocationMove(rm)
                    else:
                        terminationCondition = True
            # Swaps
            elif operator == 1:
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None:
                    if sm.moveCost < 0:
                        self.ApplySwapMove(sm)
                    else:
                        terminationCondition = True
            elif operator == 2:
                self.FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None:
                    if top.moveCost < 0:
                        self.ApplyTwoOptMove(top)
                    else:
                        terminationCondition = True

            self.TestSolution()

            if (self.sol.max_travel_time < self.bestSolution.max_travel_time):
                self.bestSolution = self.cloneSolution(self.sol)

            localSearchIterator = localSearchIterator + 1

        self.sol = self.bestSolution

    def VND(self):
        self.bestSolution = self.cloneSolution(self.sol)
        VNDIterator = 0
        kmax = 3
        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()
        neighborhoodTypeDict = {self.FindBestRelocationMove: rm, self.FindBestSwapMove: sm, self.FindBestTwoOptMove: top}

        k = 1
        neighborhoodTypeOrder = [self.FindBestSwapMove, self.FindBestTwoOptMove, self.FindBestRelocationMove]

        while k <= kmax and VNDIterator <= 100:
            self.InitializeOperators(rm, sm, top)

            moveTypeToApply = neighborhoodTypeOrder[k - 1]
            moveStructure = neighborhoodTypeDict[moveTypeToApply]
            bestNeighbor, moveCost = self.FindBestNeighbor(moveTypeToApply, moveStructure)
            if bestNeighbor is not None and moveCost < 0.0:
                self.ApplyMove(moveStructure)
                self.TestSolution()
                k = 1

                if (self.sol.max_travel_time < self.bestSolution.max_travel_time):
                    self.bestSolution = self.cloneSolution(self.sol)

                SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                VNDIterator = VNDIterator + 1
            else:
                k = k + 1

            self.searchTrajectory.append(self.sol.max_travel_time)

        SolDrawer.drawTrajectory(self.searchTrajectory)

    def FindBestNeighbor(self, moveTypeToApply, moveStructure):
        bestNeighbor = None

        moveTypeToApply(moveStructure)

        if isinstance(moveStructure, RelocationMove):
            bestNeighbor = moveStructure.originRoutePosition
        elif isinstance(moveStructure, SwapMove):
            bestNeighbor = moveStructure.positionOfFirstRoute
        elif isinstance(moveStructure, TwoOptMove):
            bestNeighbor = moveStructure.positionOfFirstRoute

        return bestNeighbor, moveStructure.moveCost

    def ApplyMove(self, moveStructure):
        if isinstance(moveStructure, RelocationMove):
            self.ApplyRelocationMove(moveStructure)
        elif isinstance(moveStructure, SwapMove):
            self.ApplySwapMove(moveStructure)
        elif isinstance(moveStructure, TwoOptMove):
            self.ApplyTwoOptMove(moveStructure)

    def cloneRoute(self, rt:Truck):
        cloned = Truck()
        cloned.AddNode(self.depot)
        cloned.travel_time = rt.travel_time
        cloned.kgOnTruck = rt.kgOnTruck
        cloned.nodesOnRoute = rt.nodesOnRoute.copy()
        return cloned

    def cloneSolution(self, sol: Solution):
        cloned = Solution()
        for i in range (0, len(sol.trucks)):
            rt = sol.trucks[i]
            clonedRoute = self.cloneRoute(rt)
            cloned.trucks.append(clonedRoute)
        cloned.travel_time = self.sol.max_travel_time
        return cloned

    def FindBestRelocationMove(self, rm):
        for originRouteIndex in range(0, len(self.sol.trucks)):
            rt1:Truck = self.sol.trucks[originRouteIndex]
            for targetRouteIndex in range (0, len(self.sol.trucks)):
                rt2:Truck = self.sol.trucks[targetRouteIndex]
                for originNodeIndex in range (1, len(rt1.nodesOnRoute)):
                    for targetNodeIndex in range (0, len(rt2.nodesOnRoute)):

                        if originRouteIndex == targetRouteIndex and (targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        A = rt1.nodesOnRoute[originNodeIndex - 1]
                        B = rt1.nodesOnRoute[originNodeIndex]

                        if rt1 != rt2:
                            if rt2.kgOnTruck + B.demand > self.capacity:
                                continue

                        # If originNodeIndex is not the last node of the route
                        if originNodeIndex != len(rt1.nodesOnRoute) - 1:
                            C = rt1.nodesOnRoute[originNodeIndex + 1]
                        # If we reached the last node of the route, there's not an originNodeIndex + 1 node (depot)
                        else:
                            C = False

                        F = rt2.nodesOnRoute[targetNodeIndex]

                        # If targetNodeIndex is not the last node of the route
                        if targetNodeIndex != len(rt2.nodesOnRoute) - 1:
                            G = rt2.nodesOnRoute[targetNodeIndex + 1]
                        # If we reached the last node of the route, there's not a targetNodeIndex + 1 node (depot)
                        else:
                            G = False

                        if not C and not G:
                            continue

                        if C and G:
                            costAdded = self.distanceMatrix[A.id][C.id] + self.distanceMatrix[F.id][B.id] + self.distanceMatrix[B.id][G.id]
                            costRemoved = self.distanceMatrix[A.id][B.id] + self.distanceMatrix[B.id][C.id] + self.distanceMatrix[F.id][G.id]

                            originRtCostChange = self.distanceMatrix[A.id][C.id] - self.distanceMatrix[A.id][B.id] - self.distanceMatrix[B.id][C.id]
                            targetRtCostChange = self.distanceMatrix[F.id][B.id] + self.distanceMatrix[B.id][G.id] - self.distanceMatrix[F.id][G.id]

                        if not C:
                            costAdded = self.distanceMatrix[F.id][B.id] + self.distanceMatrix[B.id][G.id]
                            costRemoved = self.distanceMatrix[A.id][B.id] + self.distanceMatrix[F.id][G.id]

                            originRtCostChange = 0 - self.distanceMatrix[A.id][B.id]
                            targetRtCostChange = self.distanceMatrix[F.id][B.id] + self.distanceMatrix[B.id][G.id] - self.distanceMatrix[F.id][G.id]

                        if not G:
                            costAdded = self.distanceMatrix[A.id][C.id] + self.distanceMatrix[F.id][B.id]
                            costRemoved = self.distanceMatrix[A.id][B.id] + self.distanceMatrix[B.id][C.id]

                            originRtCostChange = self.distanceMatrix[A.id][C.id] - self.distanceMatrix[A.id][B.id] - self.distanceMatrix[B.id][C.id]
                            targetRtCostChange = self.distanceMatrix[F.id][B.id]

                        moveCost = costAdded - costRemoved

                        if (moveCost < rm.moveCost) and abs(moveCost) > 0.0001:
                            self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm)

        return rm.originRoutePosition

    def FindBestSwapMove(self, sm):
        for firstRouteIndex in range(0, len(self.sol.trucks)):
            rt1:Truck = self.sol.trucks[firstRouteIndex]
            for secondRouteIndex in range (firstRouteIndex, len(self.sol.trucks)):
                rt2:Truck = self.sol.trucks[secondRouteIndex]
                for firstNodeIndex in range(1, len(rt1.nodesOnRoute)):
                    startOfSecondNodeIndex = 1
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    for secondNodeIndex in range(startOfSecondNodeIndex, len(rt2.nodesOnRoute)):

                        a1 = rt1.nodesOnRoute[firstNodeIndex - 1]
                        b1 = rt1.nodesOnRoute[firstNodeIndex]

                        if firstNodeIndex != len(rt1.nodesOnRoute) - 1:
                            c1 = rt1.nodesOnRoute[firstNodeIndex + 1]
                        else:
                            c1 = False

                        a2 = rt2.nodesOnRoute[secondNodeIndex - 1]
                        b2 = rt2.nodesOnRoute[secondNodeIndex]

                        if secondNodeIndex != len(rt2.nodesOnRoute) - 1:
                            c2 = rt2.nodesOnRoute[secondNodeIndex + 1]
                        else:
                            c2 = False

                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        if rt1 == rt2:
                            if firstNodeIndex == secondNodeIndex - 1:
                                if c2:
                                    costRemoved = self.distanceMatrix[a1.id][b1.id] + self.distanceMatrix[b1.id][b2.id] + self.distanceMatrix[b2.id][c2.id]
                                    costAdded = self.distanceMatrix[a1.id][b2.id] + self.distanceMatrix[b2.id][b1.id] + self.distanceMatrix[b1.id][c2.id]
                                else:
                                    costRemoved = self.distanceMatrix[a1.id][b1.id] + self.distanceMatrix[b1.id][b2.id]
                                    costAdded = self.distanceMatrix[a1.id][b2.id] + self.distanceMatrix[b2.id][b1.id]

                                moveCost = costAdded - costRemoved
                            else:
                                if c1:
                                    costRemoved1 = self.distanceMatrix[a1.id][b1.id] + self.distanceMatrix[b1.id][c1.id]
                                    costAdded1 = self.distanceMatrix[a1.id][b2.id] + self.distanceMatrix[b2.id][c1.id]
                                else:
                                    costRemoved1 = self.distanceMatrix[a1.id][b1.id]
                                    costAdded1 = self.distanceMatrix[a1.id][b2.id]

                                if c2:
                                    costRemoved2 = self.distanceMatrix[a2.id][b2.id] + self.distanceMatrix[b2.id][c2.id]
                                    costAdded2 = self.distanceMatrix[a2.id][b1.id] + self.distanceMatrix[b1.id][c2.id]
                                else:
                                    costRemoved2 = self.distanceMatrix[a2.id][b2.id]
                                    costAdded2 = self.distanceMatrix[a2.id][b1.id]

                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                        else:
                            if rt1.kgOnTruck - b1.demand + b2.demand > self.capacity:
                                continue
                            if rt2.kgOnTruck - b2.demand + b1.demand > self.capacity:
                                continue

                            if c1:
                                costRemoved1 = self.distanceMatrix[a1.id][b1.id] + self.distanceMatrix[b1.id][c1.id]
                                costAdded1 = self.distanceMatrix[a1.id][b2.id] + self.distanceMatrix[b2.id][c1.id]
                            else:
                                costRemoved1 = self.distanceMatrix[a1.id][b1.id]
                                costAdded1 = self.distanceMatrix[a1.id][b2.id]

                            if c2:
                                costRemoved2 = self.distanceMatrix[a2.id][b2.id] + self.distanceMatrix[b2.id][c2.id]
                                costAdded2 = self.distanceMatrix[a2.id][b1.id] + self.distanceMatrix[b1.id][c2.id]
                            else:
                                costRemoved2 = self.distanceMatrix[a2.id][b2.id]
                                costAdded2 = self.distanceMatrix[a2.id][b1.id]

                            costChangeFirstRoute = costAdded1 - costRemoved1
                            costChangeSecondRoute = costAdded2 - costRemoved2

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                        
                        if moveCost < sm.moveCost and abs(moveCost) > 0.0001:
                            self.StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)

    def ApplyRelocationMove(self, rm: RelocationMove):

        oldCost = self.CalculateTotalCost(self.sol)

        originRt = self.sol.trucks[rm.originRoutePosition]
        targetRt = self.sol.trucks[rm.targetRoutePosition]

        B = originRt.nodesOnRoute[rm.originNodePosition]

        if originRt == targetRt:
            del originRt.nodesOnRoute[rm.originNodePosition]
            if (rm.originNodePosition < rm.targetNodePosition):
                targetRt.nodesOnRoute.insert(rm.targetNodePosition, B)
            else:
                targetRt.nodesOnRoute.insert(rm.targetNodePosition + 1, B)

            originRt.travel_time += rm.moveCost
        else:
            del originRt.nodesOnRoute[rm.originNodePosition]
            targetRt.nodesOnRoute.insert(rm.targetNodePosition + 1, B)
            originRt.travel_time += rm.costChangeOriginRt
            targetRt.travel_time += rm.costChangeTargetRt
            originRt.kgOnTruck -= B.demand
            targetRt.kgOnTruck += B.demand

        self.sol.CalculateMaxTravelTime(self.model)

        newCost = self.CalculateTotalCost(self.sol)
        #debuggingOnly
        if abs((newCost - oldCost) - rm.moveCost) > 0.0001:
            print('Cost Issue')


    def ApplySwapMove(self, sm):
       oldCost = self.CalculateTotalCost(self.sol)
       rt1 = self.sol.trucks[sm.positionOfFirstRoute]
       rt2 = self.sol.trucks[sm.positionOfSecondRoute]
       b1 = rt1.nodesOnRoute[sm.positionOfFirstNode]
       b2 = rt2.nodesOnRoute[sm.positionOfSecondNode]
       rt1.nodesOnRoute[sm.positionOfFirstNode] = b2
       rt2.nodesOnRoute[sm.positionOfSecondNode] = b1

       if (rt1 == rt2):
           rt1.travel_time += sm.moveCost
       else:
           rt1.travel_time += sm.costChangeFirstRt
           rt2.travel_time += sm.costChangeSecondRt
           rt1.kgOnTruck = rt1.kgOnTruck - b1.demand + b2.demand
           rt2.kgOnTruck = rt2.kgOnTruck + b1.demand - b2.demand


       self.sol.CalculateMaxTravelTime(self.model)

       newCost = self.CalculateTotalCost(self.sol)
       # debuggingOnly
       if abs((newCost - oldCost) - sm.moveCost) > 0.0001:
           print('Cost Issue')

    def ReportSolution(self, sol):
        for i in range(0, len(sol.trucks)):
            rt = sol.trucks[i]
            for j in range (0, len(rt.nodesOnRoute)):
                print(rt.nodesOnRoute[j].id, end=' ')
            print(rt.travel_time)
        print (self.sol.max_travel_time)

    def GetLastOpenRoute(self):
        if len(self.sol.trucks) == 0:
            return None
        else:
            return self.sol.trucks[-1]

    def IdentifyBestInsertion(self, bestInsertion, rt):
        for i in range(0, len(self.service_locations)):
            candidateCust:Node = self.service_locations[i]
            if candidateCust.isRouted is False:
                if rt.kgOnTruck + candidateCust.demand <= rt.capacity:
                    lastNodePresentInTheRoute = rt.nodesOnRoute[-2]
                    trialCost = self.distanceMatrix[lastNodePresentInTheRoute.id][candidateCust.id]
                    if trialCost < bestInsertion.cost:
                        bestInsertion.customer = candidateCust
                        bestInsertion.route = rt
                        bestInsertion.cost = trialCost

    def ApplyCustomerInsertion(self, insertion):
        insCustomer = insertion.customer
        rt = insertion.route
        #before the second depot occurrence
        insIndex = len(rt.nodesOnRoute) - 1
        rt.nodesOnRoute.insert(insIndex, insCustomer)

        beforeInserted = rt.nodesOnRoute[-3]

        costAdded = self.distanceMatrix[beforeInserted.id][insCustomer.id] + self.distanceMatrix[insCustomer.id][self.depot.id]
        costRemoved = self.distanceMatrix[beforeInserted.id][self.depot.id]

        rt.travel_time += costAdded - costRemoved
        self.sol.max_travel_time += costAdded - costRemoved

        rt.kgOnTruck += insCustomer.demand

        insCustomer.isRouted = True

    def StoreBestRelocationMove(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm:RelocationMove):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost

    def StoreBestSwapMove(self, firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm):
        sm.positionOfFirstRoute = firstRouteIndex
        sm.positionOfSecondRoute = secondRouteIndex
        sm.positionOfFirstNode = firstNodeIndex
        sm.positionOfSecondNode = secondNodeIndex
        sm.costChangeFirstRt = costChangeFirstRoute
        sm.costChangeSecondRt = costChangeSecondRoute
        sm.moveCost = moveCost

    def CalculateTotalCost(self, sol):
        c = 0
        for i in range (0, len(sol.trucks)):
            rt = sol.trucks[i]
            for j in range (0, len(rt.nodesOnRoute) - 1):
                a = rt.nodesOnRoute[j]
                b = rt.nodesOnRoute[j + 1]
                c += self.distanceMatrix[a.id][b.id]
        return c

    def InitializeOperators(self, rm, sm, top):
        rm.Initialize()
        sm.Initialize()
        top.Initialize()

    def FindBestTwoOptMove(self, top):
        for rtInd1 in range(0, len(self.sol.trucks)):
            rt1:Truck = self.sol.trucks[rtInd1]
            for rtInd2 in range(rtInd1, len(self.sol.trucks)):
                rt2:Truck = self.sol.trucks[rtInd2]
                for nodeInd1 in range(0, len(rt1.nodesOnRoute)):
                    start2 = 0
                    if (rt1 == rt2):
                        start2 = nodeInd1 + 2

                    for nodeInd2 in range(start2, len(rt2.nodesOnRoute)):
                        moveCost = 10 ** 9

                        A = rt1.nodesOnRoute[nodeInd1]

                        if nodeInd1 != len(rt1.nodesOnRoute) - 1:
                            B = rt1.nodesOnRoute[nodeInd1 + 1]
                        else:
                            B = False

                        K = rt2.nodesOnRoute[nodeInd2]

                        if nodeInd2 != len(rt2.nodesOnRoute) - 1:
                            L = rt2.nodesOnRoute[nodeInd2 + 1]
                        else:
                            L = False

                        if rt1 == rt2:
                            if nodeInd1 == 0 and nodeInd2 == len(rt1.nodesOnRoute) - 1:
                                continue

                            if not L or not B:
                                continue

                            costAdded = self.distanceMatrix[A.id][K.id] + self.distanceMatrix[B.id][L.id]
                            costRemoved = self.distanceMatrix[A.id][B.id] + self.distanceMatrix[K.id][L.id]
                            moveCost = costAdded - costRemoved
                        else:
                            if nodeInd1 == 0 and nodeInd2 == 0:
                                continue

                            if nodeInd1 == len(rt1.nodesOnRoute) - 1 and nodeInd2 == len(rt2.nodesOnRoute) - 1:
                                continue

                            if not L or not B:
                                continue

                            if self.CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):
                                continue

                            costAdded = self.distanceMatrix[A.id][L.id] + self.distanceMatrix[B.id][K.id]
                            costRemoved = self.distanceMatrix[A.id][B.id] + self.distanceMatrix[K.id][L.id]
                            moveCost = costAdded - costRemoved

                        if moveCost < top.moveCost and abs(moveCost) > 0.0001:
                            self.StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top)

    def CapacityIsViolated(self, rt1, nodeInd1, rt2, nodeInd2):
        rt1FirstSegmentLoad = 0
        for i in range(0, nodeInd1 + 1):
            n = rt1.nodesOnRoute[i]
            rt1FirstSegmentLoad += n.demand
        rt1SecondSegmentLoad = rt1.kgOnTruck - rt1FirstSegmentLoad

        rt2FirstSegmentLoad = 0
        for i in range(0, nodeInd2 + 1):
            n = rt2.nodesOnRoute[i]
            rt2FirstSegmentLoad += n.demand
        rt2SecondSegmentLoad = rt2.kgOnTruck - rt2FirstSegmentLoad

        if (rt1FirstSegmentLoad + rt2SecondSegmentLoad > 3000):
            return True
        if (rt2FirstSegmentLoad + rt1SecondSegmentLoad > 3000):
            return True

        return False

    def StoreBestTwoOptMove(self, rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top):
        top.positionOfFirstRoute = rtInd1
        top.positionOfSecondRoute = rtInd2
        top.positionOfFirstNode = nodeInd1
        top.positionOfSecondNode = nodeInd2
        top.moveCost = moveCost

    def ApplyTwoOptMove(self, top):
        rt1:Truck = self.sol.trucks[top.positionOfFirstRoute]
        rt2:Truck = self.sol.trucks[top.positionOfSecondRoute]

        if rt1 == rt2:
            # reverses the nodes in the segment [positionOfFirstNode + 1,  top.positionOfSecondNode]
            reversedSegment = reversed(rt1.nodesOnRoute[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            #lst = list(reversedSegment)
            #lst2 = list(reversedSegment)
            rt1.nodesOnRoute[top.positionOfFirstNode + 1 : top.positionOfSecondNode + 1] = reversedSegment

            #reversedSegmentList = list(reversed(rt1.nodesOnRoute[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1]))
            #rt1.nodesOnRoute[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegmentList

            rt1.travel_time += top.moveCost

        else:
            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt1 = rt1.nodesOnRoute[top.positionOfFirstNode + 1 :]

            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt2 = rt2.nodesOnRoute[top.positionOfSecondNode + 1 :]

            del rt1.nodesOnRoute[top.positionOfFirstNode + 1 :]
            del rt2.nodesOnRoute[top.positionOfSecondNode + 1 :]

            rt1.nodesOnRoute.extend(relocatedSegmentOfRt2)
            rt2.nodesOnRoute.extend(relocatedSegmentOfRt1)

            self.UpdateRouteCostAndLoad(rt1)
            self.UpdateRouteCostAndLoad(rt2)

        self.sol.CalculateMaxTravelTime(self.model)

    def UpdateRouteCostAndLoad(self, rt: Truck):
        tc = 0
        tl = 0
        for i in range(0, len(rt.nodesOnRoute) - 1):
            A = rt.nodesOnRoute[i]
            B = rt.nodesOnRoute[i+1]
            tc += self.distanceMatrix[A.id][B.id]
            tl += A.demand
        rt.kgOnTruck = tl
        rt.travel_time = tc

    def TestSolution(self):
        totalSolCost = 0
        for r in range (0, len(self.sol.trucks)):
            rt: Truck = self.sol.trucks[r]
            rtCost = 0
            rtLoad = 0
            for n in range (0 , len(rt.nodesOnRoute) - 1):
                A = rt.nodesOnRoute[n]
                B = rt.nodesOnRoute[n + 1]
                rtCost += self.distanceMatrix[A.id][B.id]
                rtLoad += B.demand
            if abs(rtCost - rt.travel_time) > 0.0001:
                print('Route Cost problem')
            if rtLoad != rt.kgOnTruck:
                print('Route Load problem')

            if rt.travel_time > totalSolCost:
                totalSolCost = rt.travel_time

        if abs(totalSolCost - self.sol.max_travel_time) > 0.0001:
            print('Solution Cost problem')
            print(totalSolCost)
            print(self.sol.max_travel_time)
            
    def IdentifyBestInsertionAllPositions(self, bestInsertion, rt):
        for i in range(0, len(self.service_locations)):
            candidateCust: Node = self.service_locations[i]
            if candidateCust.isRouted is False:
                if rt.kgOnTruck + candidateCust.demand <= rt.capacity:
                    lastNodePresentInTheRoute = rt.nodesOnRoute[-2]
                    for j in range(0, len(rt.nodesOnRoute) - 1):
                        A = rt.nodesOnRoute[j]
                        B = rt.nodesOnRoute[j + 1]
                        costAdded = self.distanceMatrix[A.id][candidateCust.id] + self.distanceMatrix[candidateCust.id][B.id]
                        costRemoved = self.distanceMatrix[A.id][B.id]
                        trialCost = costAdded - costRemoved

                        if trialCost < bestInsertion.cost:
                            bestInsertion.customer = candidateCust
                            bestInsertion.route = rt
                            bestInsertion.cost = trialCost
                            bestInsertion.insertionPosition = j

    def ApplyCustomerInsertionAllPositions(self, insertion):
        insCustomer = insertion.customer
        rt = insertion.route
        # before the second depot occurrence
        insIndex = insertion.insertionPosition
        rt.nodesOnRoute.insert(insIndex + 1, insCustomer)
        rt.travel_time += insertion.cost
        self.sol.max_travel_time += insertion.cost
        rt.kgOnTruck += insCustomer.demand
        insCustomer.isRouted = True