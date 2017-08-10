# cave.py

import random

class Cave:
	def __init__(self):
		self._build_rooms()
		self._join_rows()
		self._join_columns()
		self._set_ladder()
		self._set_wumpus()
		self._set_gold()
		self._create_pits()
	
	def _build_rooms(self, height=4, width=4):
		"""
		The cave looks like this:
				4 x x x x
				3 x x x x
        y-axis	2 x x x x
				1 x x x x
				  1 2 3 4
				    x-axis
		"""
		self._x_boundaries = (0, width)
		self._y_boundaries = (0, height)
		self._rooms = []
		# todo: find a more pythonic way of storing and finding rooms.
		#	I want to avoid storing a pure array and just doing all the
		#	room mathematics in my head, but I cant think of a good way to do this.
		for y in range(height, 0, -1):
			for x in range(1, width + 1):
				room = Room(x, y)
				self._rooms.append(room)

	def _set_ladder(self, x=1, y=1):
		'''
		Creates a ladder. Ladders allow the agent to climb to the next cave.
		'''
		room = self.get_room(x, y)
		if not room.ladder: # if room has no ladder
			room.toggle_ladder()

	def _set_wumpus(self, num_wumpi=1):
		'''Sets up the wumpuses'''
		candidate_rooms = self.get_unoccupied_rooms()
		if num_wumpi > len(candidate_rooms):
			raise Exception("You can't fit all these wumpi in the cave!")
		for i in range(num_wumpi):
			wumpus_room = random.choice(candidate_rooms)
			self._spawn_wumpus(wumpus_room)
			candidate_rooms = self.get_unoccupied_rooms() # update candidate rooms

	def _spawn_wumpus(self, room):
		'''Handles low-level details of creating a wumpus. 
		Expects to receive an unoccupied room.
		'''
		# create the wumpus
		room.toggle_wumpus()
		# create stench in nearby rooms
		for adjacent in [room.north, room.south, room.east, room.west]:
			if isinstance(adjacent, Room):
				if not adjacent.stench:
					adjacent.toggle_stench()

	def _set_gold(self, num_gold=1):
		'''Sets up the gold'''
		candidate_rooms = self.get_unoccupied_rooms()
		if num_gold > len(candidate_rooms):
			raise Exception("Slow down, moneybags!")
		for i in range(num_gold):
			gold_room = random.choice(candidate_rooms)
			gold_room.toggle_gold()
			candidate_rooms = self.get_unoccupied_rooms() # update candidate rooms

	def _join_row(self, row):
		'''Connects a row horizontally'''
		for i in range(len(row) - 1):
			west_room, east_room = row[i], row[i + 1]
			east_room.west = west_room
			west_room.east = east_room

	def _join_rows(self):
		'''Joins all the rows in the cave'''
		for i in range(1, self._x_boundaries[1] + 1):
			row = self.get_row(i)
			self._join_row(row)

	def _join_column(self, column):
		'''Connects a column vertically'''
		for i in range(len(column) - 1):
			north_room, south_room = column[i], column[i + 1]
			north_room.south = south_room
			south_room.north = north_room

	def _join_columns(self):
		'''Joins all the columns in the cave'''
		for i in range(1, self._y_boundaries[1] + 1):
			column = self.get_column(i)
			self._join_column(column)

	def _create_pits(self):
		'''Creates pits. Each tile that isn't (1,1) has a 0.2 change of
		being a pit.
		'''
		for room in self._rooms:
			if not (room.x == 1 and room.y == 1):
				roll = random.randint(1, 5)
				if roll == 1:
					self._spawn_pit(room)

	def _spawn_pit(self, room):
		'''Handles low-level details of creating a pit.'''
		if not room.pit:
			room.toggle_pit()
		for adjacent in [room.north, room.south, room.east, room.west]:
			if isinstance(adjacent, Room):
				if not adjacent.breeze:
					adjacent.toggle_breeze()

	def get_unoccupied_rooms(self):
		room_list = []
		for room in self._rooms:
			if not room.occupied:
				room_list.append(room)
		return room_list

	def get_room(self, x, y):
		'''
		Returns the room object at the location.
		'''
		if x < self._x_boundaries[0] or x > self._x_boundaries[1]:
			raise Exception(str(x) + " is out of x boundaries: " + str(self._x_boundaries))
		if y < self._y_boundaries[0] or y > self._y_boundaries[1]:
			raise Exception(str(y) + " is out of y boundaries: " + str(self._y_boundaries))

		for room in self._rooms:
			if (room.x == x) and (room.y == y):
				return room
		raise Exception("({},{}) does not exist???".format(x, y))

	def get_row(self, y):
		'''Returns a row of rooms from 1 to max'''
		row = []
		for x in range(1, self._x_boundaries[1] + 1):
			row.append(self.get_room(x, y))
		return row

	def get_column(self, x):
		'''Returns a column of rooms from max to 1'''
		column = []
		for y in range(self._y_boundaries[1], 0, -1):
			column.append(self.get_room(x, y))
		return column

	def print(self):
		empty_line = '|     ' * self._x_boundaries[1] + '|'
		print('-' * ((6 * self._x_boundaries[1]) + 1))
		for y in range(self._y_boundaries[1], 0, -1):
			print(empty_line)
			print(empty_line)
			room_line = '|'
			for x in range(1, self._x_boundaries[1] + 1):
				room_line += '{:^5}'.format(self.room_string(x, y))
				room_line += '|'
			print(room_line)
			print(empty_line)
			print(empty_line)
			print('-' * ((6 * self._x_boundaries[1]) + 1))

	def room_string(self, x, y):
		room = self.get_room(x, y)
		result = ""
		if room.ladder:
			result += "L"
		if room.wumpus:
			result += "W"
		if room.gold:
			result += "G"
		if room.breeze:
			result += "B"
		if room.stench:
			result += "S"
		if room.pit:
			result += "P"
		return result


class Room:
	def __init__(self, x, y):
		self._north, self._south, self._east, self._west = \
			Wall(), Wall(), Wall(), Wall()
		self._x = x
		self._y = y
		self._ladder = False
		self._wumpus = False
		self._gold = False
		self._breeze = False
		self._stench = False
		self._pit = False

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def ladder(self):
		return self._ladder

	@property
	def occupied(self):
		return self._wumpus or self._gold or self._ladder

	@property
	def wumpus(self):
		return self._wumpus

	@property
	def gold(self):
		return self._gold

	@property
	def breeze(self):
		return self._breeze

	@property
	def stench(self):
		return self._stench

	@property
	def pit(self):
		return self._pit

	@property
	def north(self):
		return self._north

	@north.setter
	def north(self, value):
		if not (isinstance(value, Room) or isinstance(value, Wall)):
			raise Exception("Tried to set adjacent hallway to non-Room or -Wall.")
		self._north = value

	@property
	def south(self):
		return self._south

	@south.setter
	def south(self, value):
		if not (isinstance(value, Room) or isinstance(value, Wall)):
			raise Exception("Tried to set adjacent hallway to non-Room or -Wall.")
		self._south = value

	@property
	def east(self):
		return self._east

	@east.setter
	def east(self, value):
		if not (isinstance(value, Room) or isinstance(value, Wall)):
			raise Exception("Tried to set adjacent hallway to non-Room or -Wall.")
		self._east = value

	@property
	def west(self):
		return self._west

	@west.setter
	def west(self, value):
		if not (isinstance(value, Room) or isinstance(value, Wall)):
			raise Exception("Tried to set adjacent hallway to non-Room or -Wall.")
		self._west = value

	def toggle_ladder(self):
		self._ladder = not self._ladder

	def toggle_wumpus(self):
		self._wumpus = not self._wumpus

	def toggle_gold(self):
		self._gold = not self._gold

	def toggle_breeze(self):
		self._breeze = not self._breeze

	def toggle_stench(self):
		self._stench = not self._stench

	def toggle_pit(self):
		self._pit = not self._pit

class Wall:
	pass