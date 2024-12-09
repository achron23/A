# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    #The code is based on the algorithm given in the lectures
    solution = []
    neighbors = Stack()
    visited = set()
    neighbors.push((problem.getStartState(),solution))
    while True:
        if not problem.getStartState():
            return 0
        node,solution = neighbors.pop()
        visited.add(node)
        if problem.isGoalState(node):
            return solution
        suc = problem.getSuccessors(node)
        for item in  suc:
            if item[0] not in visited:
                sol = solution + [item[1]]         #append cant work because it mixes the different solutions.So we make the path different for every succesor
                neighbors.push((item[0],sol))

    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    solution = []
    neighbors = Queue()
    visited = []
    neighbors.push((problem.getStartState(),solution))
    while True:
        if not problem.getStartState():
            return []
        node, solution = neighbors.pop()
        visited.append(node)
        if problem.isGoalState(node):
            return solution
        suc = problem.getSuccessors(node)
        for item in suc:
            if item[0] not in visited and item[0] not in (i[0] for i in neighbors.list): #to itarate each queue's item coordinates
                sol = solution + [item[1]]
                neighbors.push((item[0],sol))



    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    from util import PriorityQueue
    solution = []
    neighbors = PriorityQueue()
    visited = set()
    neighbors.push((problem.getStartState(), solution),0)
    while True:
        if not problem.getStartState():
            return 0
        node, solution = neighbors.pop()
        visited.add(node)
        if problem.isGoalState(node):
            return solution
        suc = problem.getSuccessors(node)
        for item in suc:
            if item[0] not in visited and item[0] not in (i[2][0] for i in neighbors.heap):  # to itarate each queue's item coordinates
                sol = solution + [item[1]]
                cost = problem.getCostOfActions(sol)
                neighbors.push((item[0],sol),cost)
            elif item[0] not in visited and (item[0] in (i[2][0] for i in neighbors.heap)):
                for i in neighbors.heap:
                    if i[2][0] == item[0]:
                        oldc = problem.getCostOfActions(i[2][1])
                newc = problem.getCostOfActions(solution+[item[1]])
                if oldc > newc:
                    sol = solution+[item[1]]
                    neighbors.update((item[0],sol),newc)

    util.raiseNotDefined()
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def heurpriority(sol,heuristic,problem,item):
    return problem.getCostOfActions(sol)+heuristic(item,problem)


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    solution = []
    neighbors = PriorityQueue()
    visited = []
    neighbors.push((problem.getStartState(),solution),0)
    while True:
        if not problem.getStartState():
            return 0
        node, solution = neighbors.pop()
        if node in  visited:
            continue
        visited.append(node)
        if problem.isGoalState(node):
            return solution
        suc = problem.getSuccessors(node)
        for item in suc:
            if item[0] not in visited:
                sol = solution + [item[1]]
                neighbors.push((item[0],sol),heurpriority(sol,heuristic,problem,item[0]))




    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
