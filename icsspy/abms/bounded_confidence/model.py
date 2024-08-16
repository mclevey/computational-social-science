from mesa import Model
from mesa.time import RandomActivation

from .agents import BoundedConfidenceAgent


class BoundedConfidenceModel(Model):
    def __init__(self, N):
        super().__init__()  # Initialize the base Model class
        self.num_agents = N
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            agent = BoundedConfidenceAgent(i, self)
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()
