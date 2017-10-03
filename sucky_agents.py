import random
import numpy

import agent

class RandomAgent(agent.Agent):
    def get_move(self):
        return random.choice(self.possible_moves)


class LeftTurner(agent.Agent):
    def get_move(self):
        return 'left'

class ProgressMan(agent.Agent):
    """Really wants to move forward in life. Never looks back, doesn't even stop to grab the gold or climb a ladder"""
    def get_move(self):
        return numpy.random.choice(['left', 'right', 'forward'], 1, p=[.25, .25, .5])[0]