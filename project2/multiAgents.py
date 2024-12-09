# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        distfood = []
        distghost = []
        points = 0
        for i in newFood.asList():
            distfood.append(util.manhattanDistance(newPos,i))
        for i in successorGameState.getGhostPositions():
            distghost.append(util.manhattanDistance(newPos,i))
        for i in distfood:
            points += 1/i
        for i in distghost:
            points -=1/(i+0.1)
        return successorGameState.getScore() + points






def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """


    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def minimax(gameState, agent, depth):
            move = []

            # Terminate state #
            if not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState), 0

            # Reached max depth #
            if depth == self.depth:
                return self.evaluationFunction(gameState), 0

            # All ghosts have finised one round: increase depth(last ghost) #
            if agent == gameState.getNumAgents() - 1:
                depth += 1

            # Calculate nextAgent #

            # Last ghost: nextAgent = pacman #
            if agent == gameState.getNumAgents() - 1:
                nextAgent = self.index

            # Availiable ghosts. Pick next ghost #
            else:
                nextAgent = agent + 1

            # For every successor find minimax value #
            for action in gameState.getLegalActions(agent):

                if not move:  # First move
                    value = minimax(gameState.generateSuccessor(agent, action), nextAgent, depth)

                    # Fix result with minimax value and action #
                    move.append(value[0])
                    move.append(action)
                else:

                    # Check if miniMax value is better than the previous one #
                    value = minimax(gameState.generateSuccessor(agent, action), nextAgent, depth)

                    # Max agent: Pacman #
                    if agent == self.index:
                        if value[0] > move[0]:
                            move[0] = value[0]
                            move[1] = action

                    # Min agent: Ghost #
                    else:
                        if value[0] < move[0]:
                            move[0] = value[0]
                            move[1] = action
            return move

        return minimax(gameState, self.index, 0)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """


    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def ab(gameState, agent, depth,a,b):
            move = []

            # Terminate state #
            if not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState), 0

            # Reached max depth #
            if depth == self.depth:
                return self.evaluationFunction(gameState), 0

            # All ghosts have finised one round: increase depth(last ghost) #
            if agent == gameState.getNumAgents() - 1:
                depth += 1

            # Calculate nextAgent #

            # Last ghost: nextAgent = pacman #
            if agent == gameState.getNumAgents() - 1:
                nextAgent = self.index

            # Availiable ghosts. Pick next ghost #
            else:
                nextAgent = agent + 1

            # For every successor find minimax value #
            for action in gameState.getLegalActions(agent):

                if not move:  # First move
                    value = ab(gameState.generateSuccessor(agent, action), nextAgent, depth,a,b)

                    # Fix result with minimax value and action #
                    move.append(value[0])
                    move.append(action)

                    if agent == self.index:
                        a = max(move[0],a)
                    else :
                        b = min(move[0],b)
                else:
                    if move[0] > b and agent == self.index:
                        return move

                    if move[0] < a and agent != self.index:
                        return move

                    # Check if miniMax value is better than the previous one #
                    value = ab(gameState.generateSuccessor(agent, action), nextAgent, depth,a,b)

                    # Max agent: Pacman #
                    if agent == self.index:
                        if value[0] > move[0]:
                            move[0] = value[0]
                            move[1] = action
                        a = max(a,move[0])



                    # Min agent: Ghost #
                    else:
                        if value[0] < move[0]:
                            move[0] = value[0]
                            move[1] = action
                        b = min(b,move[0])
            return move

        return ab(gameState, self.index, 0,-float("inf"),float("inf"))[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(gameState, agent, depth):
            move = []

            # Terminate state #
            if not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState), 0

            # Reached max depth #
            if depth == self.depth:
                return self.evaluationFunction(gameState), 0

            # All ghosts have finised one round: increase depth(last ghost) #
            if agent == gameState.getNumAgents() - 1:
                depth += 1

            # Calculate nextAgent #

            # Last ghost: nextAgent = pacman #
            if agent == gameState.getNumAgents() - 1:
                nextAgent = self.index

            # Availiable ghosts. Pick next ghost #
            else:
                nextAgent = agent + 1

            # For every successor find minimax value #
            for action in gameState.getLegalActions(agent):

                if not move:  # First move
                    value = expectimax(gameState.generateSuccessor(agent, action), nextAgent, depth)


                    if agent == self.index:
                        move.append(value[0])
                        move.append(action)

                    else :
                        move.append(value[0]/len(gameState.getLegalActions(agent)))
                        move.append(action)

                else:

                    # Check if miniMax value is better than the previous one #
                    value = expectimax(gameState.generateSuccessor(agent, action), nextAgent, depth)

                    # Max agent: Pacman #
                    if agent == self.index:
                        if value[0] > move[0]:
                            move[0] = value[0]
                            move[1] = action



                    # Min agent: Ghost #
                    else:
                        move[0] += (value[0]/len(gameState.getLegalActions(agent)))
                        move[1] = action

            return move

        return expectimax(gameState, self.index, 0,)[1]


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    "*** YOUR CODE HERE ***"
    distfood = []
    distghost = []
    points = 0
    for i in food.asList():
        distfood.append(util.manhattanDistance(pos, i))
    for i in currentGameState.getGhostPositions():
        distghost.append(util.manhattanDistance(pos, i))
    for i in distfood:
        points += 1 / i
    for i in distghost:
        points -= 1 / (i + 0.1)
    return currentGameState.getScore() + points
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
