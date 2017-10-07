import time

import agent
import cli
import sucky_agents

if __name__ == '__main__':
    moves = []
    my_agent = sucky_agents.PrincessJasmine()
    move_generator = agent.get_ai_iteration_generator(my_agent, fog_on=False)

    for i in range(40):
        current_gamestate = next(move_generator)
        moves.append(current_gamestate.previous_action)

        print('TURN {:0>3}'.format(i))
        print('total points: {}'.format(current_gamestate.points))
        current_gamestate.print_state()
        print(cli.get_percept_message(current_gamestate.get_percepts()))
        print()
        print('-' * 20)
        # time.sleep(2)

    for move in moves:
        print(move)
