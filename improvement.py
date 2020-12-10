import VRPmodel as v

def improveFleetUtilization(sol,mod):  
    depot = mod.allNodes[0]
    while (len(sol.trucks)<25):
        sol.AddTruck()
        sol.trucks[len(sol.trucks)-1].AddNode(depot)
    iter = 0
    while iter < 10 :
        ltruck = sol.trucks[sol.last_truck_id]
        lnodes = ltruck.nodesOnRoute
        #calculate time-savings for removal of each node in last truck's route
        #find node with maximum saved time
        max_saving = 0
        max_id = 0
        for i in range(1,len(lnodes)-1):
            saving = mod.time_matrix[lnodes[i-1].id][lnodes[i+1].id] \
                - mod.time_matrix[lnodes[i-1].id][lnodes[i].id] \
                - mod.time_matrix[lnodes[i].id][lnodes[i+1].id]
            if saving > max_saving:
                max_saving = saving
                max_id = lnodes[i].id
        if mod.time_matrix[len(lnodes)-2][len(lnodes)-1] > max_saving:
            max_saving = mod.time_matrix[len(lnodes)-2][len(lnodes)-1]
            max_id = len(lnodes)-1

        max_node = lnodes[max_id]
        #select truck with least travel_time
        min_travel_time=sol.max_travel_time
        min_truck=None
        for i in range(0,len(sol.trucks)):
            if sol.trucks[i].emptySpace <= max_node.demand:
                if sol.trucks[i].travel_time < min_travel_time:
                    min_travel_time = sol.trucks[i].travel_time
                    min_truck=sol.trucks[i]
        #calculate best position for insertion
        positionOfInsertion = -1
        minimumInsertionCost = 1000000
        for k in range(1, len(min_truck.nodesOnRoute)):
            before = min_truck.nodesOnRoute[k-1]
            after = min_truck.nodesOnRoute[k]
            costAdded = mod.time_matrix[before.id][max_node.id] + mod.time_matrix[max_node.id][after.id]
            costRemoved = mod.time_matrix[before.id][after.id]
            trialCost = costAdded - costRemoved
            if trialCost < minimumInsertionCost:
                positionOfInsertion = k
                minimumInsertionCost = trialCost
        if mod.time_matrix[min_truck.nodesOnRoute[len(min_truck.nodesOnRoute)-1].id][max_node.id]< minimumInsertionCost:
            positionOfInsertion = len(min_truck.nodesOnRoute)
            minimumInsertionCost = mod.time_matrix[min_truck.nodesOnRoute[len(min_truck.nodesOnRoute)-1].id][max_node.id]
        #insert node in new position
        min_truck.nodesOnRoute.insert(positionOfInsertion, max_node)
        min_truck.travel_time += minimumInsertionCost
        min_truck.kgOnTruck += max_node.demand
        min_truck.emptySpace -= max_node.demand
        iter+=1
        #remove node from previous position
        lnodes.remove(max_node)
        ltruck.travel_time -= max_saving
        ltruck.kgOnTruck -= max_node.demand
        ltruck.emptySpace += max_node.demand
        sol.CalculateMaxTravelTime(mod)
        print(sol.max_travel_time)
    
    #recalculate longest route