import pulp


# Create a list of coordinates from file
def readFile(inputFile):
    # This will be a list of tuples with the coordinates
    coordList = []
    # Read file and create a node list
    with open(inputFile) as inputFile:
        for line in inputFile:
            if line == 'NODE_COORD_SECTION\n':
                break
        for line in inputFile:
            if line == 'EOF\n':
                break
            line = line.split()[1:]
            coordList.append((float(line[0]), float(line[1])))

    return coordList

def costMatrix(coordinates, size):
    costs = []
    for i in range(size):
        pass


def main():
    # Get list of coordinates from file
    inputFile = 'data/burma14.tsp'
    coordinates = readFile(inputFile)
    print(coordinates)

    # Number of nodes
    nNodes = len(coordinates)
    #print(coordinates)

    # Calculate matrix
    costs = []


if __name__ == '__main__':
    main()




    #print(line, end='')


'''

# Problem
my_lp_problem = pulp.LpProblem("My LP Problem", pulp.LpMaximize)

# Creating variables
x = pulp.LpVariable('x', lowBound=0, cat='Continuous')
y = pulp.LpVariable('y', lowBound=2, cat='Continuous')

# Objective function
my_lp_problem += 4 * x + 3 * y, "Z"

# Constraints
my_lp_problem += 2 * y <= 25 - x
my_lp_problem += 4 * y >= 2 * x - 8
my_lp_problem += y <= 2 * x - 5
# Make the problema infeasible
#my_lp_problem += y <= 1
# Make the problema unbounded. You have to comment the other constraints
#my_lp_problem += x <= 3

# Print problem
print(my_lp_problem)

# Print status
print(pulp.LpStatus[my_lp_problem.status])
# Solve problem
my_lp_problem.solve()
# Print status
print(pulp.LpStatus[my_lp_problem.status])

# Print solution
for variable in my_lp_problem.variables():
    print("{} = {}".format(variable.name, variable.varValue))

# Print value of solution
print(pulp.value(my_lp_problem.objective))

'''
