from enum import Enum

import mesa


class State(Enum):
    AGREE = 1
    DISAGREE = 0


class ThresholdAgent(mesa.Agent):
    """Agent representing an individual with a threshold for adopting a behavior."""

    def __init__(self, unique_id, model, state, threshold):
        super().__init__(unique_id, model)
        self.state = state
        self.threshold = threshold

    def step(self):
        """
        Decide whether to adopt the behavior based on neighbors' states and own threshold
        """
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=False)
        agree_count = sum(1 for agent in neighbors if agent.state == State.AGREE)
        agree_ratio = agree_count / len(neighbors) if neighbors else 0

        if agree_ratio >= self.threshold:
            self.state = State.AGREE
        else:
            self.state = State.DISAGREE
