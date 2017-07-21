from game import Agent
from game import Directions
import random

class DumbAgent(Agent):
	def getAction(self, state):
		return Directions.WEST
		return Directions.EAST



		# print "Location ", state.getPacmanPosition()
		# print "Actions available", state.getLegalPacmanActions()
		# print random_move = random.choice(state.getLegalPacmanActions())
		# if random_move == 'Stop':

		# return Directions
		# if Directions.WEST in state.getLegalPacmanActions():
		# 	return Directions.WEST
		# else:
		# 	return Directions.STOP