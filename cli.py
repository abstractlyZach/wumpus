import gamestate


def run_game(fog_on=False):
    game_state = gamestate.GameState(fog_on=fog_on)
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
        try:
            for i in range(command_iterations):
                handle_command(game_state, command)
        except InvalidCommandException as e:
            print(e)
        except gamestate.DevModeException as e:
            print(e)
        game_state.print()
        print('player: {}'.format(game_state.player_location))
        print('facing: {}'.format(game_state.player_orientation))
        print('total points: {}'.format(game_state.points))
        print(game_state.get_percepts())
        input_string = input('next move? ')


def handle_command(game_state, command):
    '''Parses the command string and executes the action.'''
    if command == 'left' or command == 'l':
        game_state.turn_left()
    elif command == 'right'or command == 'r':
        game_state.turn_right()
    elif command == 'forward' or command == 'f':
        game_state.move_forward()
    elif command == 'shoot' or command == 's':
        game_state.shoot()
    elif command == 'grab' or command == 'g':
        game_state.grab()
    elif command == 'climb' or command == 'c':
        game_state.climb()
    elif command == 'devmode':
        game_state.toggle_dev_mode()
    elif command == 'fog':
        game_state.toggle_fog()
    else:
        raise InvalidCommandException('InvalidCommandException: {} is not a valid command'.foramt(command))

class InvalidCommandException(Exception):
    pass