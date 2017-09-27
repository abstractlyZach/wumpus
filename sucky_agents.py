import random

import agent

class RandomAgent(agent.Agent):
    def get_move(self):
        return random.choice(self.possible_moves)


class LeftTurner(agent.Agent):
    def get_move(self):
        return 'left'