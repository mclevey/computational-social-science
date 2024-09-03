from mesa import Agent, Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation


class SIRAgent(Agent):
    def __init__(
        self, unique_id, model, recovery_time_range=(8, 12), max_agent_step_size=1
    ):

        super().__init__(unique_id, model)
        self.state = "S"
        self.infected_time = 0
        self.recovery_time_range = recovery_time_range
        self.max_agent_step_size = max_agent_step_size
        self.pos_history = []
        self.interactions = {}

    def step(self):
        if self.state == "I":
            self.infected_time += 1
            # check if agent is within the recovery window
            if self.infected_time >= self.recovery_time_range[0]:
                # if so, recover probabilistically
                if (
                    self.random.random() < 0.5
                    or self.infected_time >= self.recovery_time_range[1]
                ):
                    self.state = "R"

            # if still infected, try to infect others
            if self.state == "I":
                neighbors = self.model.grid.get_neighbors(
                    self.pos, moore=True, include_center=False
                )
                for neighbor in neighbors:
                    if (
                        neighbor.state == "S"
                        and self.random.random() < self.model.infection_rate
                    ):
                        neighbor.state = "I"

        possible_moves = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False, radius=self.max_agent_step_size
        )

        new_position = self.random.choice(possible_moves)
        self.model.grid.move_agent(self, new_position)
        self.pos_history.append(new_position)

        # record interactions with other agents in this step
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False
        )

        for neighbor in neighbors:
            if neighbor.unique_id in self.interactions:
                self.interactions[neighbor.unique_id] += 1
            else:
                self.interactions[neighbor.unique_id] = 1


class SIRModel(Model):
    def __init__(
        self,
        grid_width,
        grid_height,
        N,
        infection_rate,
        recovery_time_range,
        max_agent_step_size=1,
        n_initial_infections=1,
        max_iterations=1000,
        change_threshold=0.001,
    ):

        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(grid_width, grid_height, True)
        self.schedule = RandomActivation(self)
        self.infection_rate = infection_rate
        self.recovery_time_range = recovery_time_range
        self.max_agent_step_size = max_agent_step_size
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.change_threshold = change_threshold
        # track the ratio of infected agents in the previous step
        self.previous_infected_ratio = None

        # create agents
        for i in range(self.num_agents):
            # half the agents will have a large step size, half small
            step_size = max_agent_step_size if i % 2 == 0 else 1
            a = SIRAgent(i, self, recovery_time_range, max_agent_step_size=step_size)
            self.grid.place_agent(
                a,
                (
                    self.random.randrange(self.grid.width),
                    self.random.randrange(self.grid.height),
                ),
            )
            # initialize the position history with the starting position
            a.pos_history.append(a.pos)
            self.schedule.add(a)

        # randomly infect a specified number of agents
        initial_infected_agents = self.random.sample(
            self.schedule.agents, n_initial_infections
        )
        for agent in initial_infected_agents:
            agent.state = "I"
            agent.infected_time = 0  # initialize infection duration

        self.datacollector = DataCollector(
            model_reporters={
                "Susceptible": lambda m: self.count_state("S"),
                "Infected": lambda m: self.count_state("I"),
                "Recovered": lambda m: self.count_state("R"),
            },
            agent_reporters={
                "State": "state",
                "Infection_Duration": "infection_duration",
            },
        )
        # this line is necessary for doing multiple model runs simultaneously
        # we will do this later in the lecture
        self.running = True

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.current_iteration += 1

        # check for stopping condition based on maximum iterations
        if self.current_iteration >= self.max_iterations:
            self.running = False

        # check for stopping condition based on change in infected ratio
        current_infected_ratio = self.count_state("I")
        if self.previous_infected_ratio is not None:
            change = abs(current_infected_ratio - self.previous_infected_ratio)
            if change < self.change_threshold:
                self.running = False
        self.previous_infected_ratio = current_infected_ratio

    def count_state(self, state_name):
        count = sum([1 for a in self.schedule.agents if a.state == state_name])
        return count / self.num_agents
