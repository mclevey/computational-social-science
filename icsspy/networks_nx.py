import logging
from collections import Counter
from typing import Tuple

import networkx as nx
import pandas as pd


def create_mention_network_nx(
    df: pd.DataFrame,
    user_id_col: str = "user",
    comment_text_col: str = "comment_text",
    drop_isolates: bool = True,
    include_mentioned_no_comment_nodes: bool = True,
) -> Tuple[nx.DiGraph, pd.DataFrame]:
    G = nx.DiGraph()

    # extract all mentions
    df["mentioned_users"] = df[comment_text_col].str.findall(r"@(\w+)")
    # explode the df so that each mention becomes a separate row
    exploded_df = df.explode("mentioned_users").dropna(subset=["mentioned_users"])

    users = df[user_id_col].unique()
    G.add_nodes_from(users)

    if include_mentioned_no_comment_nodes:
        mentioned_users = exploded_df["mentioned_users"].unique()
        G.add_nodes_from(mentioned_users)

    # create edge list with weights
    edges = exploded_df[exploded_df[user_id_col] != exploded_df["mentioned_users"]]
    edge_list = edges[[user_id_col, "mentioned_users"]].values.tolist()

    # count the number of times each user mentions another user (i.e., weights)
    edge_weights = Counter((user, mentioned_user) for user, mentioned_user in edge_list)

    # add edges to the graph with weights
    for (user, mentioned_user), weight in edge_weights.items():
        G.add_edge(user, mentioned_user, weight=weight)

    # remove isolates if drop_isolates is true
    if drop_isolates:
        isolates = list(nx.isolates(G))
        G.remove_nodes_from(isolates)

    logging.info(
        (
            "Created Mentions Network\n"
            f"Number of nodes: {G.number_of_nodes()}\n"
            f"Number of edges: {G.number_of_edges()}\n"
            f"Density: {nx.density(G): .4f}\n"
        )
    )

    weighted_edges_df = pd.DataFrame(
        [
            (user, mentioned_user, weight)
            for (user, mentioned_user), weight in edge_weights.items()
        ],
        columns=[user_id_col, "mentioned_users", "weight"],
    )

    weighted_edges_df.sort_values("weight", ascending=False, inplace=True)

    return G, weighted_edges_df


def read_weighted_edgelist(
    file_path: str,
    source_col: str = "author",
    target_col: str = "mentioned_users",
    weight_col: str = "weight",
) -> nx.DiGraph:
    df = pd.read_csv(file_path)
    # check for required columns
    if not {source_col, target_col, weight_col}.issubset(df.columns):
        raise ValueError(
            f"Input file must contain '{source_col}', '{target_col}', and '{weight_col}'"
        )

    G = nx.DiGraph()
    for _, row in df.iterrows():
        try:
            G.add_edge(row[source_col], row[target_col], weight=float(row[weight_col]))
        except ValueError:
            continue

    return G
