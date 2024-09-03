import numpy as np
from mesa import Agent, Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation


class BoundedConfidenceAgent(Agent):
    def __init__(self, unique_id, model, epsilon, max_agent_step_size=1):
        super().__init__(unique_id, model)
        self.opinion = self.random.uniform(
            -1, 1
        )  # Agent's opinion initialized between -1 and 1
        self.epsilon = epsilon  # Confidence bound ($\epsilon$)
        self.max_agent_step_size = max_agent_step_size  # Step size for movement
        self.pos_history = []  # Track agent's position over time
        self.interactions = {}  # Track interactions with a count

    def step(self):
        # Move to a random neighboring cell with the given step size
        possible_moves = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False, radius=self.max_agent_step_size
        )
        new_position = self.random.choice(possible_moves)
        self.model.grid.move_agent(self, new_position)
        self.pos_history.append(new_position)  # Record the new position

        # Interact with neighbors within confidence bound
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False
        )
        for neighbor in neighbors:
            if abs(self.opinion - neighbor.opinion) <= self.epsilon:
                # Update opinion if within confidence bound
                self.opinion = (self.opinion + neighbor.opinion) / 2

            # Record interactions
            if neighbor.unique_id in self.interactions:
                self.interactions[neighbor.unique_id] += 1
            else:
                self.interactions[neighbor.unique_id] = 1


class BoundedConfidenceModel(Model):
    def __init__(
        self,
        grid_width,
        grid_height,
        N,
        epsilon,
        max_agent_step_size=1,
        max_steps=1000,
        convergence_threshold=0.001,
    ):
        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(grid_width, grid_height, True)
        self.schedule = RandomActivation(self)
        self.epsilon = epsilon
        self.max_agent_step_size = max_agent_step_size
        self.max_steps = max_steps
        self.convergence_threshold = convergence_threshold

        # Initialize step_count
        self.step_count = 0  # This will track the number of steps taken

        # Create agents
        for i in range(self.num_agents):
            step_size = (
                max_agent_step_size if i % 2 == 0 else 1
            )  # Half agents have large step size, half small
            agent = BoundedConfidenceAgent(
                i, self, epsilon, max_agent_step_size=step_size
            )
            self.grid.place_agent(
                agent,
                (
                    self.random.randrange(self.grid.width),
                    self.random.randrange(self.grid.height),
                ),
            )
            agent.pos_history.append(
                agent.pos
            )  # Initialize the position history with the starting position
            self.schedule.add(agent)

        self.datacollector = DataCollector(
            agent_reporters={"Opinion": "opinion"},
            model_reporters={"Avg_Similarity": self.calculate_similarity},
        )

    def calculate_similarity(self):
        """Calculate average pairwise similarity in agent opinions."""
        opinions = np.array([agent.opinion for agent in self.schedule.agents])
        pairwise_diffs = np.abs(opinions[:, None] - opinions[None, :])
        similarity = 1 - pairwise_diffs  # Similarity is inverse of difference
        avg_similarity = np.mean(similarity)
        return avg_similarity

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.step_count += 1

        # Check stopping conditions
        if self.check_convergence() or self.step_count >= self.max_steps:
            self.running = False

    def check_convergence(self):
        """Check if the opinions have converged."""
        opinions = np.array([agent.opinion for agent in self.schedule.agents])
        max_diff = np.max(np.abs(opinions[:, None] - opinions[None, :]))
        return max_diff < self.convergence_threshold
