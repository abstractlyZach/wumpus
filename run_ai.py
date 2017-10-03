import time

import agent
import cli
import sucky_agents

if __name__ == '__main__':
    my_agent = sucky_agents.PrincessJasmine()
    move_generator = agent.get_ai_iteration_generator(my_agent)

    for i in range(15):
        current_gamestate = next(move_generator)

        print('TURN {:0>3}'.format(i))
        print('total points: {}'.format(current_gamestate.points))
        current_gamestate.print_state()
        print(cli.get_percept_message(current_gamestate.get_percepts()))
        print()
        print('-' * 20)
        time.sleep(2)
