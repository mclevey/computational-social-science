# NEED TO FILTER ENTITIES, NEEDS TO HAPPEN UPSTREAM IN ENT TASK...

# import pandas as pd
# import yaml

# import icsspy
# import icsspy.networks as networks
# from icsspy.utils import lists_to_strings, strings_to_lists

# logger = icsspy.initialize_logger()

# with open("construct_channel_networks.yaml", "r") as file:
#     task_config = yaml.safe_load(file)


# global_edge_threshold = task_config.get("bipartite_edge_threshold")

# topic_info = pd.read_csv("../input/channels_topic_info.csv")

# df = pd.read_csv("../input/channels_merged_labelled_text.csv")
# df.dropna(subset=["entities_list"], inplace=True)
# df["entities_list"] = strings_to_lists(df["entities_list"])


# df_grouped = df.groupby("channel")
# topic_info_grouped = topic_info.groupby("channel")

# all_wels = []
# for channel in df_grouped.groups.keys():
#     entity_group = df_grouped.get_group(channel)

#     topic_info_group = topic_info_grouped.get_group(channel).copy()
#     topic_info_group.drop(columns="Count", inplace=True)

#     entity_topic_edgelist = networks.create_bipartite_edgelist(
#         df=entity_group, topic_col="topic", entity_list_col="entities_list"
#     )

#     # drop the BERTopic junk topic
#     entity_topic_edgelist = entity_topic_edgelist[entity_topic_edgelist["Topic"] != -1]

#     entity_topic_edgelist["Channel"] = channel

#     entity_topic_edgelist = pd.merge(
#         entity_topic_edgelist, topic_info_group, on="Topic", how="left"
#     )

#     topic_representation_model = task_config.get("topic_representation", "Name")
#     entity_topic_edgelist[topic_representation_model] = lists_to_strings(
#         entity_topic_edgelist[topic_representation_model]
#     )

#     g, wel = networks.construct_topic_entity_network(
#         entity_topic_edgelist, "Entity", topic_representation_model, "Count"
#     )

#     edges_to_remove = [
#         edge for edge in g.edges() if g.ep.weight[edge] < global_edge_threshold
#     ]
#     for edge in edges_to_remove:
#         g.remove_edge(edge)

#     logger.info(
#         (
#             f"Created Topic-Entity Network for '{channel}'\n"
#             f"Used edge threshold: {global_edge_threshold}\n"
#             f"Number of nodes: {g.num_vertices()}\n"
#             f"Number of edges: {g.num_edges()}\n"
#         )
#     )

#     wel["channel"] = channel
#     wel = wel[wel["Count"] > global_edge_threshold]
#     all_wels.append(wel)

#     output_network = f"../output/channels_{channel}_[bipartite]_entity_topic_network"
#     networks.save_gt(g, output_network)

# all_wel = pd.concat(all_wels)

# all_wel.to_csv("../output/channels_[bipartite]_all_entity_entity_wels.csv", index=False)
# print(all_wel.head(30))
