# test_gamestate.py

import gamestate

game_state = gamestate.GameState(fog_on=True)

input_string = 'abc'
while input_string != 'q':
	args = input_string.split(' ')
	command = args[0]
	if len(args) == 1:
		command_iterations = 1
	elif len(args) == 2:
		command_iterations = int(args[1])
	else:
		print('command not recognized')
		continue
	for i in range(command_iterations):
		if command == 'left':
			game_state.turn_left()
		elif command == 'right':
			game_state.turn_right()
		elif command == 'forward':
			game_state.move_forward()
		elif command == 'shoot':
			game_state.shoot()
		elif command == 'grab':
			game_state.grab()
		elif command == 'climb':
			game_state.climb()
		else:
			print('command not recognized: {}'.format(input_string))
	game_state.print()
	print('player: {}'.format(game_state.player_location))
	print('facing: {}'.format(game_state.player_orientation))
	print('total points: {}'.format(game_state.points))
	print(game_state.get_percepts())
	input_string = input('next move? ')