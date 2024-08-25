import random

import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid
from mesa.time import RandomActivation

from .agents import State, ThresholdAgent


class ThresholdModel(Model):
    """Model simulating a threshold-based decision-making process on a network."""

    def __init__(
        self,
        network,
        num_initial_agree,
        threshold_alpha=2,
        threshold_beta=5,
        saturation_point=0.95,
        max_steps=100,
    ):
        super().__init__()
        self.network = network
        self.num_initial_agree = num_initial_agree
        self.saturation_point = saturation_point
        self.max_steps = max_steps
        self.grid = NetworkGrid(self.network)
        self.schedule = RandomActivation(self)
        self.running = True

        # Convert nodes to a list for random sampling
        nodes_list = list(self.network.nodes())

        # Assign initial states and thresholds
        initial_agents = random.sample(nodes_list, self.num_initial_agree)
        threshold_dist = self.generate_thresholds_distribution(
            len(nodes_list), threshold_alpha, threshold_beta
        )

        for i, node in enumerate(nodes_list):
            state = State.AGREE if node in initial_agents else State.DISAGREE
            threshold = threshold_dist[i]
            agent = ThresholdAgent(node, self, state=state, threshold=threshold)
            self.schedule.add(agent)
            self.grid.place_agent(agent, node)

        # Data collection
        self.datacollector = DataCollector(
            model_reporters={
                "num_agree": lambda m: self.count_type(State.AGREE),
                "num_disagree": lambda m: self.count_type(State.DISAGREE),
                "frac_agree": lambda m: self.count_type(State.AGREE)
                / len(self.schedule.agents),
                "frac_disagree": lambda m: self.count_type(State.DISAGREE)
                / len(self.schedule.agents),
            }
        )

    @staticmethod
    def generate_thresholds_distribution(num_agents, alpha, beta):
        """Generate a list of threshold values based on a Beta distribution."""
        return list(np.random.beta(alpha, beta, num_agents))

    def count_type(self, state):
        """Count the number of agents in a given state."""
        return sum(1 for agent in self.schedule.agents if agent.state == state)

    def step(self):
        """Advance the model by one step and check for stopping conditions."""
        self.datacollector.collect(self)
        self.schedule.step()

        # Get the most recent collected data for frac_agree and frac_disagree
        model_data = self.datacollector.get_model_vars_dataframe().iloc[-1]
        frac_agree = model_data["frac_agree"]
        frac_disagree = model_data["frac_disagree"]

        # Check if agreement or disagreement fraction has reached the saturation point
        if (
            frac_agree >= self.saturation_point
            or frac_disagree >= self.saturation_point
            or self.schedule.steps >= self.max_steps
        ):
            self.running = False
