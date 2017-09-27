import gamestate


def run_game(fog_on=False):
    """Runs the game through the CLI."""
    game_state = gamestate.GameState(fog_on=fog_on)
    input_string = 'pass'
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
        print('total points: {}'.format(game_state.points))
        game_state.print_state()
        percepts = game_state.get_percepts()
        print(get_percept_message(percepts))
        # print('player: {}'.format(game_state.player_location))
        # print('facing: {}'.format(game_state.player_orientation))
        # print(game_state.get_percepts())
        input_string = input('Next move? ')


def get_percept_message(percepts):
    """Return a string based on the set of percepts for the turn."""
    message_list = []
    if percepts.glitter:
        message_list.append('You see something glittering on the ground.')
    if percepts.breeze:
        message_list.append('You feel a cool breeze.')
    if percepts.scream:
        message_list.append('You hear a gut-wrenching scream.')
    if percepts.bump:
        message_list.append('Your face hurts. You ran into a wall.')
    if percepts.stench:
        message_list.append("PEEYEWWWWWW! What's that smell?! Something rank lurks nearby...")
    if message_list == []:
        message_list.append("You don't feel a thing. You monster.")
    return '\n'.join(message_list)

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
    elif command == 'pass':
        pass
    else:
        raise InvalidCommandException('InvalidCommandException: {} is not a valid command'.format(command))

class InvalidCommandException(Exception):
    pass
