# gamestate.py

DIRECTIONS = ['north', 'east', 'south', 'west']

import cave

class GameState:
	def __init__(self):
		self._new_cave()
		
	def _new_cave(self):
		self._cave = cave.Cave()
		self._current_room = self._cave.get_room(1, 1)
		self._current_orientation = 'east'

	def _next_room(self, current_room=self._current_room):
		'''Returns the next room, which can be a Room or a Wall'''
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

	# =======================================================================
	# actions

	def move_forward(self):
		'''Moves the player forward'''
		next_room = self._next_room()
		if isinstance(next_room, cave.Wall):
			self._current_room = starting_room

	def turn_left(self):
		current_direction_index = DIRECTIONS.index(self._current_orientation)
		self._current_orientation = DIRECTIONS[(current_direction_index - 1) % 4]

	def turn_right(self):
		current_direction_index = DIRECTIONS.index(self._current_orientation)
		self._current_orientation = DIRECTIONS[(current_direction_index + 1) % 4]

	def grab(self):
		'''Grabs gold if it's on the ground'''
		if self._current_room.gold:
			# grab gold
			self._current_room.toggle_gold()
			pass

	def shoot(self):
		'''Fire the arrow in the current direction'''
		next_room = self._next_room()
		while not isinstance(next_room, Wall) and not next_room.wumpus:
			next_room = self._next_room(next_room)
		if isinstance(next_room, Wall):
			# clink! (no sound)
			pass
		elif next_room.wumpus:
			# wumpus dead. wumpus SCREAMS
			# need to write code in Cave to clean up wumpus
			pass

	def climb(self):
		'''Attempt to climb a ladder'''
		if self._current_room.ladder:
			self._new_cave()
			# notify player?

	# end actions
	# =======================================================================

	@property
	def player_location(self):
		'''Returns the coordinates of the player's location'''
		return (self._current_room.x, self._current_room.y)

	@property
	def player_orientation(self):
		'''Returns the player's current orientation'''
		return self._current_orientation
