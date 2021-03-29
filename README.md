# OptMethods-Assignment

## Overview
This repository contains the assignment delivered for Optimization Methods in Management Science course. The course is part of the curriculum of the [Department of Management Science & Technology](https://www.dept.aueb.gr/en/dmst) from the Athens University of Economics and Business and the project is assigned by Emmanouil Zachariadis.

## Instructions
To run the code of the project, you must have python 3 installed. After downloading the code, cd to the directory it is saved and execute the file named **vrp.py**

## The problem
* A VRP (vehicle routing problem) is assumed, where 200 locations need to be served using a fleet of 25 trucks.
* Each truck's capacity is 3 tonnes and they all leave the storage facilities simultaneously.
* Each service location has different procurement needs which have to be met by a single truck visit.
* The trucks' assumed travelling speed is 35 km/h.
* Each service location has its own estimated unloading time to deliver the goods. This can either be 5, 15, or 25 minutes.
* The goal is to minimize the service time for the last location to receive the goods. (**minmax problem**)
* The point of view is to generate a good quality solution in very little time. Thus the implementation will exit after 5 minutes.

## The designed solution
* After randomly generating the service locations using an object list and a distance matrix, we transformed the distances into time by taking account unloading durations too.
* Then a first feasible solution was created by applying a **Best Fit heuristic**. The solution is constructed by iteratively adding each location to the truck that would suffer the least increase in its travelling time. This strategy results in a solution of 12 hours. This means that the last service location would receive products after 12 hours.
* The initial solution is improved by treating each truck's route as a **TSP problem** and rearranging the order of the locations in each truck's itinerary separately. This brings us to 8.952 hours.
* Another heuristic is also applied: finding the location that causes the greatest delay in the truck that arrives last and adding it to the truck that finishes its scheduled trip first. After 20 iterations the algorithm plateaus at 6.664 hours
* Next, a **VND algorithm (Variable Neighborhood Descent)** is used. We used three different move types: SwapMove, TwoOptMove and RelocationMove. VND in a regular VRP problem would look to minimize the total service time of all trucks. This does not directly apply in our case, but it still lowers service time for the last location significantly.
* At the same time, whenever the classic VND implementation gets stuck in a local optimum (which is detected by a tabu list of size 5), an **alternative VND implementation** takes over, which considers only moves that originate from the truck that arrives last. Here moves are selected based on their effect on the travel time of the last truck. If no move decreases the last truck's finish time, no move is seleted.
* Until total execution time reaches 5 minutes, the last two algorithms are altrnately executed.
* The final solution scores 4.514 hours.

## Authors
* Irene Arapogiorgi
* Kiriaki Velliniati
