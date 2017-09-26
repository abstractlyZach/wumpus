class Agent(object):
    possible_moves = ['left', 'right', 'forward', 'shoot', 'grab', 'climb']
    def __init__(self):
        pass

    def handle_percepts(self, percepts):
        pass

    def get_move(self):
        pass


def poll_agent(agent, percepts):
    agent.handle_percepts(percepts)
    return agent.get_move()