import math
import pulp


# Create a list of coordinates from file. Each element will be a tuple (x,y)
def readFile(inputFile):
    # This will be a list of tuples with the coordinates
    coordList = []
    # Read file and create a node list
    with open(inputFile) as inputFile:
        # Reach start of node list
        for line in inputFile:
            if line == 'NODE_COORD_SECTION\n':
                break
        # Append coordinates to coordList
        for line in inputFile:
            if line == 'EOF\n':
                break
            line = line.split()[1:]
            coordList.append((float(line[0]), float(line[1])))
    return coordList

# Generate a matrix of costs based on the coordinates array
def costMatrix(coordinates, nNodes):
    # Create a matrix of nNodes rows and nNodes columns
    costs = [ [0 for i in range(nNodes)] for j in range(nNodes)]
    for i in range(nNodes):
        for j in range(nNodes):
            # Calculate Euclidean distance
            if i != j:
                costs[i][j] = math.sqrt((coordinates[j][0] - coordinates[i][0])**2 + (coordinates[j][1] - coordinates[i][1])**2)
    return costs

# Create a binary and integer variables
def createVariables(nNodes):
    # Create a matrix of nNodes rows and nNodes columns
    xMatrix = [ [None for i in range(nNodes)] for j in range(nNodes)]
    # Add the binary variables to the matrix
    for i in range(nNodes):
        for j in range(nNodes):
            if i != j:
                xMatrix[i][j] = pulp.LpVariable('x_{}_{}'.format(i, j), cat='Binary')

    # Create a list of nNodes integer variables
    uList =  []
    for i in range(nNodes):
        # Variable from work proposal, it's wrong
        #uList.append(pulp.LpVariable('u_{}'.format(i), lowBound=1, upBound=nNodes, cat='Integer'))
        # Variable from slides, it's right
        uList.append(pulp.LpVariable('u_{}'.format(i), lowBound=0, upBound=nNodes-1, cat='Integer'))

    return xMatrix, uList


# Add objective function
def addObjectiveFunction(problem, costs, xMatrix, nNodes):
    problem += (pulp.lpSum([ costs[i][j] * xMatrix[i][j] for i in range(nNodes) for j in range(nNodes) if i != j ]))

# Add all constraints
def addConstraints(problem, xMatrix, uList, nNodes):
    # The sum of the elements of a row in xMatrix should be 1
    for i in range(nNodes):
        problem += pulp.lpSum([ xMatrix[i][j] for j in range(nNodes) if i != j ]) == 1

    # The sum of the elements of a column in xMatrix should be 1
    for j in range(nNodes):
        problem += pulp.lpSum([ xMatrix[i][j] for i in range(nNodes) if i != j ]) == 1

    # This is the constraints from the work proposal, it's wrong
    '''
    # Constraint from the work proposal
    for i in range(1, nNodes):
        for j in range(1, nNodes):
            if i != j:
                problem += uList[i] - uList[j] + nNodes * xMatrix[i][j] <= nNodes - 1
    '''
    # Constraint from the slides, it's right
    for i in range(0, nNodes):
        for j in range(1, nNodes):
            if i != j:
                #problem += uList[i] - uList[j] + nNodes * xMatrix[i][j] <= nNodes - 1
                problem += uList[j] >= uList[i] + xMatrix[i][j] - nNodes * (1 - xMatrix[i][j])
    problem += uList[0] == 0



def main():
    # Get list of coordinates from file
    inputFile = 'data/burma14.tsp'
    coordinates = readFile(inputFile)

    # Number of nodes
    nNodes = len(coordinates)

    # Calculate matrix of costs
    costs = costMatrix(coordinates, nNodes)

    # Create the problem
    tsp = pulp.LpProblem("Travelling Salesman Problem", pulp.LpMinimize)

    xMatrix, uList = createVariables(nNodes)
    addObjectiveFunction(tsp, costs, xMatrix, nNodes)
    addConstraints(tsp, xMatrix, uList, nNodes)

    # Print status
    print(pulp.LpStatus[tsp.status])
    # Solve problem
    tsp.solve()
    # Print status
    print(pulp.LpStatus[tsp.status])


    # Print answer
    print('Answer:', [u.varValue for u in uList])

    # Print value of solution
    print('Value:', pulp.value(tsp.objective))

    '''
    # Print value of xMatrix
    resultMatrix = [ [None for i in range(nNodes)] for j in range(nNodes)]
    for i in range(nNodes):
        for j in range(nNodes):
            if i != j:
                resultMatrix[i][j] = xMatrix[i][j].varValue
    for row in resultMatrix:
        print(row)
    '''


if __name__ == '__main__':
    main()
