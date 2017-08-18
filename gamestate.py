# gamestate.py

DIRECTIONS = ['north', 'east', 'south', 'west']

import cave
from collections import namedtuple

Percepts = namedtuple('Percepts', 
					['glitter', 'breeze', 'scream', 'bump', 'stench']
					)

class GameState:
	def __init__(self):
		self._bump = False
		self._scream = False
		self._points = 0
		self._new_cave()

	def _new_cave(self):
		self._cave = cave.Cave()
		self._current_room = self._cave.get_room(1, 1)
		self._current_orientation = 'east'
		self._player_holding_gold = False

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
		self._points -= 1

	def _end_of_turn(self):
		'''Handles end-of-turn housekeeping. Death is an important one. If you end your turn
		on a wumpus or a pit tile, you die.'''
		if self._current_room.pit or self._current_room.wumpus:
			# death mechanic
			self._points -= 1000
			self._new_cave()


	# =======================================================================
	# actions

	def take_action(action_function):
		'''decorator for taking an action'''
		def turn_wrapper(self):
			self._start_of_turn()
			action_function(self)
			self._end_of_turn()
		return turn_wrapper

	@take_action
	def move_forward(self):
		'''Moves the player forward'''
		next_room = self._next_room()
		if isinstance(next_room, cave.Wall):
			# self._current_room = starting_room
			# idk what this was for ^
			self._bump = True
		else:
			self._current_room = next_room

	@take_action
	def turn_left(self):
		current_direction_index = DIRECTIONS.index(self._current_orientation)
		self._current_orientation = DIRECTIONS[(current_direction_index - 1) % 4]

	@take_action
	def turn_right(self):
		current_direction_index = DIRECTIONS.index(self._current_orientation)
		self._current_orientation = DIRECTIONS[(current_direction_index + 1) % 4]

	@take_action
	def grab(self):
		'''Grabs gold if it's on the ground'''
		if self._current_room.gold:
			# grab gold
			self._current_room.toggle_gold()
			self._player_holding_gold = True
			pass

	@take_action
	def shoot(self):
		'''Fire the arrow in the current direction'''
		self._points -= 9 # shooting arrow is total -9 points
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

	@take_action
	def climb(self):
		'''Attempt to climb a ladder'''
		if self._current_room.ladder:
			if self._player_holding_gold:
				self._points += 1000
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

	@property
	def points(self):
		'''Returns how many points the player has'''
		return self._points