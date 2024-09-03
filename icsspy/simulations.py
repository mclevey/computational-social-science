import copy
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .abms.threshold import ThresholdModel


def generate_thresholds_distribution(network, alpha, beta):
    return list(np.random.beta(alpha, beta, network.number_of_nodes()))


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
    return random.sample(
        node_list, int(round(len(node_list) * frac, 0))
    )  # randomly select nodes from node_list without replacement


def add_to_infection_set(infection_sets, fraction_increase, network):
    num_adds = int(
        round(network.number_of_nodes() * fraction_increase, 0)
    )  # Number of new initial nodes needed to be added
    new_infection_sets = []
    for inf_set in infection_sets:
        new_set = copy.deepcopy(inf_set)
        while (
            len(new_set) < len(inf_set) + num_adds
        ):  # Keep randomly selecting nodes, checking if they're already in the list,
            # and adding if they haven't until the new set is as long as needed.
            new_add = random.choice(list(network.nodes()))
            if new_add not in new_set:
                new_set.append(new_add)
        new_infection_sets.append(new_set)
    return new_infection_sets


def run_threshold_model_experiment(
    G,
    num_initial_agree_values,
    threshold_alpha,
    threshold_beta,
    saturation_point,
    max_steps,
    n_runs,
):
    """
    Runs the threshold model multiple times with varying initial conditions and collects
    the results.

    Parameters:
        G (networkx.Graph): The network to run the model on.
        num_initial_agree_values (list): List of initial agreeing agent values to test.
        threshold_alpha (float or list of tuples): Alpha parameter for the threshold
        distribution, or a list of (alpha, beta) pairs.
        threshold_beta (float or None): Beta parameter for the threshold distribution,
        if a list of tuples is not provided.
        saturation_point (float): The point at which the model stops running.
        max_steps (int): Maximum number of steps for the model to run.
        n_runs (int): Number of runs for each initial agree value.

    Returns:
        pd.DataFrame: A DataFrame with the collected results from all runs.
    """
    all_results = []
    run_id_offset = 0

    # Check if threshold_alpha is a list of tuples (indicating varying alpha-beta pairs)
    if isinstance(threshold_alpha, list) and isinstance(threshold_alpha[0], tuple):
        # Varying alpha-beta pairs
        threshold_pairs = threshold_alpha
    else:
        # Fixed alpha and beta
        threshold_pairs = [(threshold_alpha, threshold_beta)]

    for threshold_alpha, threshold_beta in threshold_pairs:
        for num_initial_agree in num_initial_agree_values:
            for i in range(n_runs):
                # Create a new model instance for each run
                model = ThresholdModel(
                    network=G,
                    num_initial_agree=num_initial_agree,
                    threshold_alpha=threshold_alpha,
                    threshold_beta=threshold_beta,
                    saturation_point=saturation_point,
                    max_steps=max_steps,
                )

                # Run the model
                for step in range(max_steps):
                    if not model.running:
                        break
                    model.step()

                    # Collect data at this step
                    run_data = (
                        model.datacollector.get_model_vars_dataframe().iloc[-1].copy()
                    )
                    run_data["Run"] = i + run_id_offset
                    run_data["num_initial_agree"] = num_initial_agree
                    run_data["Step"] = step
                    run_data["threshold_alpha"] = threshold_alpha
                    run_data["threshold_beta"] = threshold_beta
                    all_results.append(run_data)

            run_id_offset += n_runs  # Update the offset for the next set of runs

    # Combine all results into a DataFrame
    results_df = pd.DataFrame(all_results)
    return results_df
