from enum import Enum

import mesa


class State(Enum):
    AGREE = 1
    DISAGREE = 0


class Ego(mesa.Agent):
    def __init__(self, unique_id, model, state, threshold):
        super().__init__(unique_id, model)
        self.threshold = threshold
        self.state = state

    def make_adoption_decision(self):
        alters = self.model.grid.get_neighborhood(self.pos, include_center=False)
        alter_agents = self.model.grid.get_cell_list_contents(alters)
        alter_states = [a.state for a in alter_agents]
        if len(alter_states) > 0:
            local_yes_prop = alter_states.count(State.AGREE) / len(alter_states)
            if local_yes_prop >= self.threshold:
                self.state = State.AGREE
            else:
                self.state = State.DISAGREE

    def step(self):
        self.make_adoption_decision()
