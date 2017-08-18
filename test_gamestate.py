# test_gamestate.py

import gamestate

game_state = gamestate.GameState()

input_string = None
while input_string != 'q':
	if input_string == 'left':
		game_state.turn_left()
	elif input_string == 'right':
		game_state.turn_right()
	elif input_string == 'forward':
		game_state.move_forward()
	elif input_string == 'shoot':
		game_state.shoot()
	elif input_string == 'grab':
		game_state.grab()
	elif input_string == 'climb':
		game_state.climb()
	else:
		print('command not recognized: {}'.format(input_string))
	game_state._cave.print()
	print('player: {}'.format(game_state.player_location))
	print('facing: {}'.format(game_state.player_orientation))
	print('total points: {}'.format(game_state.points))
	print(game_state.get_percepts())
	input_string = input('next move? ')