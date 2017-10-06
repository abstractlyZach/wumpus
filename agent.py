import gamestate

class Agent(object):
    possible_moves = ['left', 'right', 'forward', 'shoot', 'grab', 'climb']
    def __init__(self):
        pass

    def handle_percepts(self, percepts):
        pass

    def get_move(self):
        pass


class AgentException(Exception):
    pass


def poll_agent(agent, percepts):
    agent.handle_percepts(percepts)
    return agent.get_move()


def get_ai_iteration_generator(agent, fog_on=True):
    current_state = gamestate.GameState(fog_on=fog_on)
    # yield turn 0 for the first move
    yield current_state
    while True: # no end condition defined by book
        current_percepts = current_state.get_percepts()
        agent_move = poll_agent(agent, current_percepts)
        if agent_move == 'left':
            current_state.turn_left()
        elif agent_move == 'right':
            current_state.turn_right()
        elif agent_move == 'forward':
            current_state.move_forward()
        elif agent_move == 'shoot':
            current_state.shoot()
        elif agent_move == 'grab':
            current_state.grab()
        elif agent_move == 'climb':
            current_state.climb()
        else:
            raise AgentException('Agent returned an illegal action: {}'.format(agent_move))
        yield current_state
