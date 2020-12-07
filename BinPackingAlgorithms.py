import random

class Group:
    def __init__(self, i):
        self.ID = i
        self.numberOfPersons = random.randint(10, 25)

class Solution:
    def __init__(self):
        self.buses = []

class Bus:
    def __init__(self):
        self.capacity = 0
        self.emptySpace = 0
        self.personsOnBoard = 0
        self.groupsOnBoard = []

def main():
    groupsToBeTransported = []
    random.seed(1)
    numberOfGroups = 600

    for i in range (0, numberOfGroups, 1):
        g = Group(i)
        groupsToBeTransported.append(g)

    busCapacity = 40
    sol = Solution()

    #sortGroups(groupsToBeTransported)
    FirstFit(sol, groupsToBeTransported, busCapacity)
    print(len(sol.buses))
    sol.buses.clear()

    BestFit(sol, groupsToBeTransported, busCapacity)
    print(len(sol.buses))
    sol.buses.clear()

def sortGroups(listOFGroups: list):
    listOFGroups.sort(key = lambda x: x.numberOfPersons, reverse=True)

def BestFit(sol, groupsToBeTransported, busCapacity):

    totalGroups = len(groupsToBeTransported)

    for i in range(0, totalGroups):

        toBeAssigned = groupsToBeTransported[i]
        indexOfBestBus = -1
        minimumEmptySpace = 1000000

        totalOpenBuses = len(sol.buses)

        for b in range(0, totalOpenBuses):
            trialBus = sol.buses[b]
            if (trialBus.emptySpace >= toBeAssigned.numberOfPersons):
                if (trialBus.emptySpace < minimumEmptySpace):
                    minimumEmptySpace = trialBus.emptySpace
                    indexOfBestBus = b

        if (indexOfBestBus != -1):
            busOfInsertion: Bus = sol.buses[indexOfBestBus]
            busOfInsertion.groupsOnBoard.append(toBeAssigned)
            busOfInsertion.personsOnBoard = busOfInsertion.personsOnBoard + toBeAssigned.numberOfPersons
            busOfInsertion.emptySpace = busOfInsertion.emptySpace - toBeAssigned.numberOfPersons
        else:
            newBus = Bus()
            newBus.capacity = busCapacity
            newBus.personsOnBoard = 0
            newBus.emptySpace = busCapacity

            sol.buses.append(newBus)
            newBus.groupsOnBoard.append(toBeAssigned)
            newBus.personsOnBoard = newBus.personsOnBoard + toBeAssigned.numberOfPersons
            newBus.emptySpace = newBus.emptySpace - toBeAssigned.numberOfPersons



def FirstFit(sol, groupsToBeTransported, busCapacity):
    totalGroups = len(groupsToBeTransported)

    for i in range(0, totalGroups):

        toBeAssigned = groupsToBeTransported[i]
        indexOfBusToBeInserted = -1
        totalOpenBuses = len(sol.buses)

        for b in range(0, totalOpenBuses):
            trialBus:Bus = sol.buses[b]

            if (trialBus.emptySpace >= toBeAssigned.numberOfPersons):
                indexOfBusToBeInserted = b
                break

        if (indexOfBusToBeInserted != -1):
            busOfInsertion: Bus = sol.buses[indexOfBusToBeInserted]
            busOfInsertion.groupsOnBoard.append(toBeAssigned)
            busOfInsertion.personsOnBoard = busOfInsertion.personsOnBoard + toBeAssigned.numberOfPersons
            busOfInsertion.emptySpace = busOfInsertion.emptySpace - toBeAssigned.numberOfPersons
        else:
            newBus = Bus()
            newBus.capacity = busCapacity
            newBus.personsOnBoard = 0
            newBus.emptySpace = busCapacity

            sol.buses.append(newBus)
            newBus.groupsOnBoard.append(toBeAssigned)
            newBus.personsOnBoard = newBus.personsOnBoard + toBeAssigned.numberOfPersons
            newBus.emptySpace = newBus.emptySpace - toBeAssigned.numberOfPersons




main()