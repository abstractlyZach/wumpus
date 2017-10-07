import sucky_agents

class TestDirectionAgent(object):
    def test_how_to_turn(self):
        self._agent = sucky_agents.DirectionAgent()
        # facing east
        assert self._agent.direction == 'east'
        assert self._agent.how_to_turn('east') is None
        assert self._agent.how_to_turn('north') == 'left'
        assert self._agent.how_to_turn('south') == 'right'
        assert self._agent.how_to_turn('west') == 'about face'
        # facing north
        self._agent.turn_left()
        assert self._agent.how_to_turn('north') is None
        assert self._agent.how_to_turn('west') == 'left'
        assert self._agent.how_to_turn('east') == 'right'
        assert self._agent.how_to_turn('south') == 'about face'
        # facing west
        self._agent.turn_left()
        assert self._agent.how_to_turn('west') is None
        assert self._agent.how_to_turn('south') == 'left'
        assert self._agent.how_to_turn('north') == 'right'
        assert self._agent.how_to_turn('east') == 'about face'
        # facing south
        self._agent.turn_left()
        assert self._agent.how_to_turn('south') is None
        assert self._agent.how_to_turn('east') == 'left'
        assert self._agent.how_to_turn('west') == 'right'
        assert self._agent.how_to_turn('north') == 'about face'

    def test_opposite_direction(self):
        agent = sucky_agents.DirectionAgent()
        assert agent.opposite_direction('north') == 'south'
        assert agent.opposite_direction('south') == 'north'
        assert agent.opposite_direction('east') == 'west'
        assert agent.opposite_direction('west') == 'east'
