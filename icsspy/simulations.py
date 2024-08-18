import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import random
import copy

def simulation_df(iteration_results, network, prop=True):
    population_size = network.number_of_nodes()
    trends, deltas = [], []

    for iteration in iteration_results:
        trends.append(iteration["node_count"])
        deltas.append(iteration["status_delta"])

    columns = ["Susceptible", "Infected", "Removed"]

    trends = pd.DataFrame(trends)
    trends.columns = columns
    if prop is True:
        trends = trends.div(population_size)

    deltas = pd.DataFrame(deltas)
    deltas.columns = columns

    return trends, deltas


def simulation_by_iteration_matrices(
    multi_runs, population_size, state, proportion=False
):
    """
    Constructs matrices for each status category in the model.
    Each row in the matrix represents a single simulation run.
    Each column in the matrix represents an iteration within a simulation.
    Each cell is the count (or proportion) of nodes that were in
    the state in question for that iteration of that simulation.
    """
    results = []
    for i, simulation in enumerate(multi_runs):
        sims = multi_runs[i]["trends"]["node_count"]
        results.append(sims[state])
    results = pd.DataFrame(results)
    if proportion is True:
        results = results.div(population_size)
    return results


def visualize_trends(
    multi_runs,
    network,
    states=[0, 1, 2],
    labels=["Susceptible", "Infected", "Removed"],
    highlight_state=1,
    proportion=False,
    return_data=False,
):
    """
    Gets the simulation by iteration matrix for each possible node state.
    """
    population_size = network.number_of_nodes()

    state_matrices = []
    medians = []

    for state in states:
        df = simulation_by_iteration_matrices(
            multi_runs, population_size=population_size, state=state, proportion=True
        )
        medians.append(df.median())
        df = df.T
        state_matrices.append(df)

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    lstyles = ["--", "-", "-."]

    for i in range(len(state_matrices)):
        for column in state_matrices[i].T:
            plt.plot(state_matrices[i][column], alpha=0.1, linewidth=0.5)

    for i in range(len(medians)):
        if i is highlight_state:
            plt.plot(medians[i], c="crimson", label=labels[i], linestyle=lstyles[i])
        else:
            plt.plot(medians[i], c="black", label=labels[i], linestyle=lstyles[i])

    ax.set(xlabel="Iteration", ylabel="Proportion of nodes")
    plt.legend() 
    sns.despine()
    plt.tight_layout()
    plt.show()

    if return_data is True:
        return state_matrices, medians


def rand_infection_set(network, frac):
    node_list = list(network.nodes())
    return random.sample(node_list, int(round(len(node_list)*frac, 0))) # randomly select nodes from node_list without replacement

def add_to_infection_set(infection_sets, fraction_increase, network):
    num_adds = int(round(network.number_of_nodes()*fraction_increase, 0)) # Number of new initial nodes needed to be added
    new_infection_sets = []
    for inf_set in infection_sets:
        new_set = copy.deepcopy(inf_set)
        while len(new_set) < len(inf_set) + num_adds: # Keep randomly selecting nodes, checking if they're already in the list, and adding if they haven't until the new set is as long as needed.
            new_add = random.choice(list(network.nodes()))
            if new_add not in new_set:
                new_set.append(new_add)
        new_infection_sets.append(new_set)
    return new_infection_sets



