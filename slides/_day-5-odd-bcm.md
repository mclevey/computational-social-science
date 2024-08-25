### ODD Protocol for the Bounded Confidence Model (BCM)

#### 1. **Overview**

**Purpose of the Model**:

The Bounded Confidence Model (BCM) simulates opinion dynamics in a continuous opinion space. It models how agents' opinions evolve over time through interactions with other agents within a predefined confidence bound (ε). The model is used to study phenomena such as opinion polarization, consensus formation, and the effect of varying confidence bounds on these processes.

**Entities, State Variables, and Scales**:

- **Agents**: Each agent has an **opinion** represented as a continuous value between -1 and 1, an **epsilon** representing their confidence bound, a **max_agent_step_size** representing their movement capability in a spatial grid, a **pos_history** to track their spatial positions over time, and an **interactions** dictionary to record the frequency of interactions with other agents.
- **Environment**: The agents are placed on a **MultiGrid** of size defined by **grid_width** and **grid_height**. The grid is toroidal (agents moving off one edge of the grid reappear on the opposite edge).
- **Scale**: The model runs for a user-defined number of steps (**n_iterations**). The scale of opinions is continuous between -1 and 1.

**Process Overview**:

- Agents move to new positions on the grid based on their step size.
- Agents interact with neighboring agents within their confidence bound (ε), potentially updating their opinions.
- The model tracks the evolution of opinions over time, and data is collected for further analysis.

#### 2. **Design Concepts**

**Basic Principles**:

- **Bounded Confidence**: Agents only interact with others whose opinions differ by less than a threshold value, **ε**. This models the idea that individuals are only influenced by those whose views are not too dissimilar from their own.
- **Opinion Averaging**: When two agents interact within this bound, they adjust their opinions to the average of their own and the interacting agent's opinion.

**Emergence**:

- The emergence of opinion clusters, polarization, or consensus depending on the value of **ε**.
- The effect of varying confidence bounds on the structure and distribution of opinions across the agent population.

**Adaptation**:

- Agents adapt their opinions based on interactions with their neighbors if those neighbors fall within their confidence bound.

**Objectives**:

- The primary objective for the agents is to update their opinions through interactions. The model tracks how the average pairwise opinion similarity evolves over time.

**Learning**:

- Agents do not learn in a traditional sense, but they do update their opinions based on interactions.

**Prediction**:

- Agents do not explicitly predict future states but react to the current opinions of their neighbors within the confidence bound.

**Sensing**:

- Agents can sense the opinions of their immediate neighbors on the grid.

**Interaction**:

- Interaction occurs between agents occupying neighboring grid cells, where they compare opinions and possibly adjust their own.

**Stochasticity**:

- Agents’ initial opinions are randomly assigned within the range [-1, 1].
- Movement is stochastic, with agents choosing a random neighboring cell to move to in each step.

**Collectives**:

- No formal collective structures are defined, though clusters of agents with similar opinions may emerge naturally.

**Observation**:

- The model observes and records **Opinion** for each agent at each time step.
- It also records a global measure, **Avg_Similarity**, which represents the average pairwise similarity of opinions across the population.

#### 3. **Details**

**Initialization**:

- The model initializes with **N** agents, each placed randomly on a grid of size **grid_width x grid_height**.
- Each agent’s opinion is initialized as a random value between -1 and 1.
- Agents are given a confidence bound, **ε**, which defines their bounded confidence interval.

**Input Data**:

- The model can be initialized with parameters loaded from an external YAML file. The parameters typically include the number of agents, the grid size, the confidence bound (**ε**), the maximum step size for agent movement, and the number of iterations.

**Submodels**:

- **BCMAgent**:

- The agent's **step** method handles movement, interaction with neighbors, and opinion updating.

- Each agent decides on a random new position within a certain range (defined by **max_agent_step_size**), then interacts with its neighbors within the confidence bound to potentially update its opinion.
- **BoundedConfidenceModel**:

- The **step** method handles the collection of data and agent activation for each time step.

- The model includes a method to calculate the average similarity of opinions (**calculate_similarity**), which is used to observe the convergence of opinions across the population.

### Execution of the Model

- The model runs for a predefined number of iterations, during which agents move, interact, and update their opinions. Data is collected at each step for post-simulation analysis, allowing for the observation of opinion dynamics under varying conditions of bounded confidence (**ε**).
