# test_gamestate.py

import gamestate

game_state = gamestate.GameState()

input_string = None
while input_string != 'q':
	game_state._cave.print()
	print('player: {}'.format(game_state.player_location))
	print('facing: {}'.format(game_state.player_orientation))
	print(game_state.get_percepts())
	print(exec(input('next move? ')))