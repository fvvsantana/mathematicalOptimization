# Mathematical Optimization

## Description

The proposal of this project is to solve the [Travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem) using two different approaches and compare the results.

The first one is in the file [solve.py](solve.py). It consists of an implementation of the [Miller, Tucker and Zemlin (MTZ) model](http://quanscope.com/TSP_MTZ.pdf) applied to a linear solver.

The second approach is in the file [heuristics.py](heuristics.py). We use two heuristics to find a good solution.
The first one is a constructive heuristic and it consists on always taking the neighbor that is closest to the last visited node. In the process, we need to take care of not visiting again nodes that have already been visited.
The second is a local search heuristic that is used over the solution found by the first heuristic. This heuristic starts switching neighbor nodes 2 by 2. If the solution doesn't improve because of these changes, we do exchanges 3 by 3. We continually increase the number of changed nodes on each exchange, when we see a improvement from the original solution, we stop the process and pick this better solution.

In the folder [results](results), there are the results of execution.

For more information about the model, solving process and results, checkout the [report](relatorioProgmat.pdf).

## Usage

To run this project you need to use Python 3.
To see the heuristics working, run:
```
    python heuristics.py burma14
```
Where burma14 is the name of the file that's in the folder 'data' without the extension '.tsp'.

To see the linear solver solving the problem using integral variables, run:
```
    python3 solve.py
```
It will solve also the burma14 problem.

## Tech stack
* Python (Pulp)
