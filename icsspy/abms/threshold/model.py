import logging
import random

import networkx as nx
import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid
from mesa.time import RandomActivation

from .agents import Ego, State

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def sample_threshold(distribution_of_thresholds, idx):
    if len(distribution_of_thresholds) > idx:
        return distribution_of_thresholds[idx]
    else:
        raise ValueError("Threshold distribution index out of range")


def generate_network(n, k, p, tries):
    return nx.connected_watts_strogatz_graph(n, k, p, tries, seed=36)


def initial_agree_random_selection(G, n_agree):
    return random.sample(list(G.nodes()), n_agree)


def generate_thresholds_distribution(network, alpha, beta):
    return list(np.random.beta(alpha, beta, network.number_of_nodes()))


class ThresholdModel(Model):
    def __init__(
        self,
        num_initial_AGREE,
        network,
        thresholds=None,
        threshold_alpha_beta=None,
        saturation_point=None,
        max_step_end_run=100,
    ):
        super().__init__()
        self.G = network
        self.number_of_nodes = len(self.G.nodes())
        self.nodes = list(self.G.nodes())
        self.num_initial_AGREE = num_initial_AGREE
        self.saturation_point = saturation_point
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)
        self.max_step_end_run = max_step_end_run
        self.running = True

        initial_agree_agents = self.random.sample(self.nodes, self.num_initial_AGREE)

        if thresholds is None:
            self.threshold_alpha = threshold_alpha_beta[0]
            self.threshold_beta = threshold_alpha_beta[1]

            self.distribution_of_thresholds = generate_thresholds_distribution(
                self.G, self.threshold_alpha, self.threshold_beta
            )
            logging.debug(f"Generated thresholds: {self.distribution_of_thresholds}")
        else:
            self.distribution_of_thresholds = thresholds
            logging.debug(
                f"Using external thresholds: {self.distribution_of_thresholds}"
            )

        if len(self.distribution_of_thresholds) < self.number_of_nodes:
            raise ValueError(
                "Threshold distribution does not have enough elements for all nodes"
            )

        for idx, node in enumerate(self.G.nodes()):
            state = State.AGREE if node in initial_agree_agents else State.DISAGREE
            threshold = sample_threshold(self.distribution_of_thresholds, idx)
            if threshold is None:
                raise ValueError(f"Threshold for node {node} is None")
            logging.debug(f"Assigning threshold {threshold} to node {node}")
            agent = Ego(node, self, state=state, threshold=threshold)
            self.schedule.add(agent)
            self.grid.place_agent(agent, node)

        self.datacollector = DataCollector(
            {
                "num_agree": lambda m: self.count_type(m, State.AGREE),
                "num_disagree": lambda m: self.count_type(m, State.DISAGREE),
                "frac_agree": lambda m: self.count_type(m, State.AGREE)
                / self.number_of_nodes,
                "frac_disagree": lambda m: self.count_type(m, State.DISAGREE)
                / self.number_of_nodes,
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        if (
            self.saturation_point
            and self.count_type(self, State.AGREE) / self.number_of_nodes
            > self.saturation_point
        ):
            self.running = False
        if self.count_type(self, State.DISAGREE) / self.number_of_nodes == 1:
            self.running = False
        if self.count_type(self, State.AGREE) / self.number_of_nodes == 1:
            self.running = False
        if self.schedule.steps >= self.max_step_end_run:
            self.running = False

    @staticmethod
    def count_type(model, node_state):
        count = 0
        for node in model.schedule.agents:
            if node.state == node_state:
                count += 1
        return count
