import random
import numpy

import agent
import gamestate

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


class DeathAware(agent.Agent):
    def __init__(self):
        self._previous_score = 0




class LocationAware(agent.Agent):
    """Knows its place in the world"""
    def __init__(self):
        self._previous_score = 0
        self._new_cave()
        super().__init__()

    def handle_percepts(self, percepts):
        """Takes in percepts and moves the agent to a new cave if it dies"""
        new_score = percepts.points
        if self._previous_score - new_score >= 1000:
            self._new_cave()
        self._previous_score = new_score

    def _new_cave(self):
        self._direction = 'east'
        self._coordinates = (0, 0)
        self._unvisited = set()
        for x in range(4):
            for y in range(4):
                self._unvisited.add((x, y))
        self._unvisited.remove((0, 0))

    @property
    def direction(self):
        return self._direction

    @property
    def coordinates(self):
        return self._coordinates

    def turn_left(self):
        direction_index = gamestate.DIRECTIONS.index(self._direction)
        self._direction = gamestate.DIRECTIONS[(direction_index - 1) % 4]

    def turn_right(self):
        direction_index = gamestate.DIRECTIONS.index(self._direction)
        self._direction = gamestate.DIRECTIONS[(direction_index + 1) % 4]

    def move_forward(self):
        self._coordinates = self.forward_prediction()
        self._unvisited.remove(self._coordinates)

    def forward_prediction_after_turn(self, turn_direction):
        """Predict where the agent will be after a turn and a forward move"""
        if turn_direction == 'left':
            self.turn_left()
        elif turn_direction == 'right':
            self.turn_right()
        else:
            raise Exception("You didn't enter a valid direction: {}".format(turn_direction))
        prediction = self.forward_prediction()
        # reset direction
        if turn_direction == 'left':
            self.turn_right()
        elif turn_direction == 'right':
            self.turn_left()
        return prediction

    def forward_prediction(self):
        """Predict where the agent will be after this move"""
        if self._direction == 'east':
            vector = (1, 0)
        elif self._direction == 'north':
            vector = (0, 1)
        elif self._direction == 'west':
            vector = (-1, 0)
        elif self._direction == 'south':
            vector = (0, -1)
        next_room = (self._coordinates[0] + vector[0], self._coordinates[1] + vector[1])
        if self.is_room_out_of_bounds(next_room):
            return self._coordinates
        else:
            return next_room

    def is_room_out_of_bounds(self, coordinates):
        x, y = coordinates
        if x > 3 or x < 0:
            return True
        if y > 3 or y < 0:
            return True
        return False


class PrincessJasmine(LocationAware):
    """She can't go back to where she used to be."""
    def get_move(self):
        print('current location: {}'.format(self.coordinates))
        print('going forward puts me at {}'.format(self.forward_prediction()))
        print('unvisited rooms: {}'.format(self._unvisited))
        print('{} unvisited rooms'.format(len(self._unvisited)))

        if (self.forward_prediction() in self._unvisited) and (self.forward_prediction() != self._coordinates):
            self.move_forward()
            return'forward'
        elif self.forward_prediction_after_turn('left') in self._unvisited:
            self.turn_left()
            return 'left'
        elif self.forward_prediction_after_turn('right') in self._unvisited:
            self.turn_right()
            return 'right'
        else:
            # if she feels trapped, she just starts moping and examining the floor
            return 'grab'
