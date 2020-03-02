from solve import costMatrix, readFile
from sys import argv
from typing import List, Tuple, Iterator, Optional
from time import time
from itertools import permutations

def greedyHeuristic(costs: List[List[float]]) -> Tuple[List[int], float]:
    ''' Solve the TSP using a greedy heuristic. Returns the path and the final cost. '''

    unvisited = set(i for i in range(1, len(costs)))
    current = 0
    path = [current]
    totalCost = 0

    while unvisited:
        # Get the next node to be visited from current node and its cost
        next_, cost = min(zip(unvisited, (costs[current][i] for i in unvisited)), key=lambda p: p[1])
        path.append(next_)
        unvisited.remove(next_)
        totalCost += cost
        current = next_

    # Return to the origin
    totalCost += costs[current][0]

    return path, totalCost

def generateSolutions(path: List[int]) -> Iterator[List[int]]:
    ''' Generate all the possible permutations of the initial solution, from closest to furthest '''

    aux = list(path)
    sol = set()
    sol.add(tuple(aux))
    for tam in range(2, len(path)):
        for init in range(1, len(path)-tam+1):
            for perm in permutations(aux[init:init+tam]):
                aux[init:init+tam] = list(perm)
                if tuple(aux) not in sol:
                    sol.add(tuple(aux))
                    yield aux
                aux = list(path)

def calculateCost(costs: List[List[float]], path: List[int]) -> float:
    ''' Returns the total cost of the path '''

    current = path[0]
    cost = 0
    for node in path[1:]:
        cost += costs[current][node]
        current = node

    return cost


def improvementHeuristic(costs: List[List[float]], path: List[int], oldCost: float) -> Optional[Tuple[List[int], float]]:
    ''' Find a better solution for the TSP using a enhancement heuristic. Returns the new path and cost if there's any. '''

    for sol in generateSolutions(path):
        newCost = calculateCost(costs, sol)
        if newCost < oldCost:
            return sol, newCost
    return None


def main():
    # Get list of coordinates from file
    inputFile = 'data/' + argv[1] + '.tsp'
    coordinates = readFile(inputFile)
    print('Problem:', inputFile)

    # Number of nodes
    nNodes = len(coordinates)
    print('Number of nodes:', nNodes)

    # Calculate matrix of costs
    costs = costMatrix(coordinates, nNodes)
    #print('Costs matrix:', costs)
    #for row in costs:
    #    print(list(map(lambda p: round(p, 2), row)))
    #print()

    startTime = time()
    # Solve the TSP with heuristics
    path, totalCost = greedyHeuristic(costs)
    elapsedTime = time() - startTime

    print('Anwser:', path)
    print('Value:', totalCost)
    print('Time to solve:', elapsedTime, 'seconds\n')

    startTime = time()
    # Try to find a better solution
    tupl = improvementHeuristic(costs, path, totalCost)
    elapsedTime = time() - startTime

    if tupl is not None:
        print('New solution:', tupl[0])
        print('New value:', tupl[1])
        print('Time to solve:', elapsedTime, 'seconds\n')

if __name__ == '__main__':
    main()
