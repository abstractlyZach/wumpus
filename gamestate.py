# gamestate.py

DIRECTIONS = ['north', 'east', 'south', 'west']

import cave
from collections import namedtuple

Percepts = namedtuple('Percepts', 
					['glitter', 'breeze', 'scream', 'bump', 'stench']
					)

class GameState:
	def __init__(self):
		self._new_cave()

	def _new_cave(self):
		self._cave = cave.Cave()
		self._current_room = self._cave.get_room(1, 1)
		self._current_orientation = 'east'
		self._start_of_turn()

	def _next_room(self, current_room=None):
		'''Returns the next room, which can be a Room or a Wall'''
		if not current_room:
			current_room = self._current_room
		if self._current_orientation == 'west':
			return current_room.west
		elif self._current_orientation == 'east':
			return current_room.east
		elif self._current_orientation == 'north':
			return current_room.north
		elif self._current_orientation == 'south':
			return current_room.south
		else:
			raise Exception("Player isn't facing one of the cardinal directions! \
							 He's facing: {}.".format(self._current_orientation))

	def _start_of_turn(self):
		'''Handle start-of-turn housekeeping, like turning 
		off the scream or the bumping'''
		self._bump = False
		self._scream = False

	# =======================================================================
	# actions

	def move_forward(self):
		'''Moves the player forward'''
		self._start_of_turn()
		next_room = self._next_room()
		if isinstance(next_room, cave.Wall):
			# self._current_room = starting_room
			# idk what this was for ^
			self._bump = True
		else:
			self._current_room = next_room

	def turn_left(self):
		self._start_of_turn()
		current_direction_index = DIRECTIONS.index(self._current_orientation)
		self._current_orientation = DIRECTIONS[(current_direction_index - 1) % 4]

	def turn_right(self):
		self._start_of_turn()
		current_direction_index = DIRECTIONS.index(self._current_orientation)
		self._current_orientation = DIRECTIONS[(current_direction_index + 1) % 4]

	def grab(self):
		'''Grabs gold if it's on the ground'''
		self._start_of_turn()
		if self._current_room.gold:
			# grab gold
			self._current_room.toggle_gold()
			pass

	def shoot(self):
		'''Fire the arrow in the current direction'''
		self._start_of_turn()
		next_room = self._next_room()
		while not isinstance(next_room, cave.Wall) and not next_room.wumpus:
			next_room = self._next_room(next_room)
		if isinstance(next_room, cave.Wall):
			# clink! (no sound)
			pass
		elif next_room.wumpus:
			# wumpus dead. wumpus SCREAMS
			self._scream = True
			self._cave.kill_wumpus(next_room)
			pass

	def climb(self):
		'''Attempt to climb a ladder'''
		self._start_of_turn()
		if self._current_room.ladder:
			self._new_cave()
			# notify player?

	# end actions
	# =======================================================================

	def get_percepts(self):
		'''Returns the set of percepts after an action is taken.'''
		# set scream
		# set bump
		percepts = Percepts(glitter=self._current_room.gold, 
						breeze=self._current_room.breeze, 
						stench=self._current_room.stench, 
						scream=self._scream,
						bump=self._bump)
		# print(percepts)
		return percepts

	@property
	def player_location(self):
		'''Returns the coordinates of the player's location'''
		return (self._current_room.x, self._current_room.y)

	@property
	def player_orientation(self):
		'''Returns the player's current orientation'''
		return self._current_orientation
