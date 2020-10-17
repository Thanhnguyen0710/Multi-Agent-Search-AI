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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        
        score = successorGameState.getScore()
        food = newFood.asList()
        minFood = 0
        for i in food:
          dist = abs(newPos[0] - i[0]) + abs(newPos[1] - i[1]) 
          if minFood == 0 or minFood > dist:
            minFood = dist
        
        minGhost = 0
        for i in newGhostStates:
          dist = abs(newPos[0] - i.getPosition()[0]) + abs(newPos[1] - i.getPosition()[1]) 
          if minGhost == 0 or minGhost > dist:
            minGhost = dist

        score = score - 1/(minGhost + 0.1) + 1/(minFood + 0.1) + min(newScaredTimes)
        return score 

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        
        def get_max( gameState, depth, agentIndex) :
          depth = depth - 1
          if depth < 0 or gameState.isLose() or gameState.isWin():
            return (self.evaluationFunction(gameState), None)
          else :
            v = float('-inf')
            max_action = None
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
              successor = gameState.generateSuccessor(agentIndex, action)
              new_v = get_min(successor, depth, agentIndex+1)[0]
              if v < new_v:
                v = new_v
                max_action = action
            return v, max_action 

        def get_min( gameState, depth, agentIndex) :
          if depth < 0 or gameState.isLose() or gameState.isWin():
            return (self.evaluationFunction(gameState), None)
          else :
            v = float('inf')
            min_action = None
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
              successor = gameState.generateSuccessor(agentIndex, action)
              new_v = None 
              if agentIndex != gameState.getNumAgents()-1:
                new_v = get_min(successor, depth, agentIndex+1)[0]
              else : 
                new_v = get_max(successor, depth, 0)[0]
              if v > new_v:
                v = new_v
                min_action = action
            return v, min_action 

        return get_max(gameState, self.depth, 0)[1]
      

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def get_max( gameState, depth, agentIndex, alpha, beta) :
          depth = depth - 1
          if depth < 0 or gameState.isLose() or gameState.isWin():
            return (self.evaluationFunction(gameState), None)
          else :
            v = float('-inf')
            max_action = None
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
              successor = gameState.generateSuccessor(agentIndex, action)
              new_v = get_min(successor, depth, agentIndex+1, alpha, beta)[0]
              if v < new_v:
                v = new_v
                max_action = action
              if v > beta : return v,max_action
              alpha = max(alpha,v)
            return v, max_action 

        def get_min( gameState, depth, agentIndex, alpha, beta) :
          if depth < 0 or gameState.isLose() or gameState.isWin():
            return (self.evaluationFunction(gameState), None)
          else :
            v = float('inf')
            min_action = None
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
              successor = gameState.generateSuccessor(agentIndex, action)
              new_v = None 
              if agentIndex != gameState.getNumAgents()-1:
                new_v = get_min(successor, depth, agentIndex+1, alpha, beta)[0]
              else : 
                new_v = get_max(successor, depth, 0, alpha, beta)[0]
              if v > new_v:
                v = new_v
                min_action = action
              if v < alpha: return v, min_action 
              beta = min(beta, v)
            return v, min_action 

        return get_max(gameState, self.depth, 0, float('-inf'), float('inf'))[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions()
        best_score = float('-inf')
        best_action  = None
        for action in actions:
          successor = gameState.generateSuccessor(0, action)
          score = self.get_score(successor, 0, 1)
          if best_score < score:
            best_score = score
            best_action = action
        return best_action

    def get_max(self, gameState, depth):
      if(depth == self.depth or gameState.isLose() or gameState.isWin()) :
        return self.evaluationFunction(gameState)

      actions = gameState.getLegalActions()
      scores = []
      for action in actions:
        successor = gameState.generateSuccessor(0, action)
        scores.append(self.get_score(successor, depth, 1))

      return max(scores)

    def get_score(self, gameState, depth, agentIndex):
      if(depth == self.depth or gameState.isLose() or gameState.isWin()) :
        return self.evaluationFunction(gameState)

      actions = gameState.getLegalActions(agentIndex)
      score = []
      for action in actions:
        successor = gameState.generateSuccessor(agentIndex, action)
        new_score = 0
        if agentIndex != gameState.getNumAgents() - 1:
          new_score = self.get_score(successor, depth, agentIndex + 1)
        else :
          new_score = self.get_max(successor, depth + 1)
        score.append(new_score)
      return sum(score) / len(score)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foods = newFood.asList()
    visited = []
    min_cost = 0
    currentPosPacman = newPos

    while len(visited) != len(foods):
      min_food = None 
      min_dist = 0

      for food in foods:
        dist = abs(currentPosPacman[0] - food[0]) + abs(currentPosPacman[1] - food[1])
        if food not in visited and ( min_dist > dist or min_dist == 0 ):
          min_food = food
          min_dist = dist

      currentPosPacman = min_food
      visited.append(min_food)
      min_cost = min_cost + min_dist

    minDistGhost = 0

    for stateGhost in newGhostStates:
      min_dist = abs(stateGhost.getPosition()[0] - newPos[0]) + abs(stateGhost.getPosition()[1] - newPos[1])
      if minDistGhost == 0 or min_dist < minDistGhost:
        minDistGhost = min_dist

    return currentGameState.getScore() + 1/ (min_cost + 0.1) - 1/ (minDistGhost + 0.1) + min(newScaredTimes)

# Abbreviation
better = betterEvaluationFunction

