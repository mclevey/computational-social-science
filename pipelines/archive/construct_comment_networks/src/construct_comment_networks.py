# import ast

# import pandas as pd

# import icsspy
# import icsspy.networks as networks
# import icsspy.text as text

# # import yaml


# # with open("construct_comment_networks.yaml", "r") as file:
# #     task_config = yaml.safe_load(file)

# logger = icsspy.initialize_logger()

# merged = pd.read_csv("../input/comments_merged_labelled_text.csv")
# # merged.dropna(subset=["entities_list"], inplace=True)
# # # convert 'entities_list' column from strings to lists
# # merged["entities_list"] = merged["entities_list"].apply(
# #     lambda x: ast.literal_eval(x) if isinstance(x, str) else x
# # )

# channels = pd.read_csv("../input/channels_processed.csv")
# print(channels.info())

# channels = channels[["video_id", "channel"]]
# merged = pd.merge(merged, channels, on="video_id", how="left")

# # print(merged.info())


# # all_b_wels = []
# all_m_wels = []

# for channel, group_df in merged.groupby("channel"):
#     #     # CONSTRUCT BIPARTITE NETWORKS #
#     #     bipartite_threshold = 2

#     #     # Topic-Entity Network

#     #     ent_top_el = text.entity_topic_edgelist(
#     #         group_df, topic_col="topic", entities_col="entities_list"
#     #     )

#     #     ent_top_el.columns = ["Topic", "Entity", "Weight (Topic-Entity Count)"]

#     #     # get topic information
#     #     topic_info = pd.read_csv("../input/comments_topic_info.csv")
#     #     topic_info.drop(columns="Count", inplace=True)
#     #     entity_topic_edges = pd.merge(ent_top_el, topic_info, on="Topic", how="left")

#     #     # construct network
#     #     g, wel = networks.create_topic_entity_network(
#     #         entity_topic_edges, "Entity", "Name", "Weight (Topic-Entity Count)"
#     #     )

#     #     edges_to_remove = [
#     #         edge for edge in g.edges() if g.ep.weight[edge] < bipartite_threshold
#     #     ]

#     #     for edge in edges_to_remove:
#     #         g.remove_edge(edge)

#     #     logger.info(
#     #         (
#     #             f"Created Topic-Entity Network for '{channel}'\n"
#     #             f"Used edge threshold (bipartite): {bipartite_threshold}\n"
#     #             f"Number of nodes: {g.num_vertices()}\n"
#     #             f"Number of edges: {g.num_edges()}\n"
#     #         )
#     #     )

#     #     wel["Channel"] = channel
#     #     wel = wel[wel["Weight (Topic-Entity Count)"] > bipartite_threshold]
#     #     all_b_wels.append(wel)

#     #     output_network = f"../output/comments_{channel}_entity_topic_network"
#     #     networks.save_gt(g, output_network)

#     #     # block model was here...

#     #     # CONSTRUCT MENTION NETWORKS #
#     mention_threshold = 2

#     group_df["author"] = group_df["author"].str.replace("@", "")

#     g_mention, edges = networks.construct_mention_network(
#         df=group_df,
#         user_id_col="author",
#         comment_text_col="processed_text",
#     )

#     edges.columns = ["Author", "Mentioned Users", "Weight"]
#     edges = edges[edges["Weight"] > mention_threshold]
#     edges["Channel"] = channel

#     mention_edges_to_remove = [
#         edge
#         for edge in g_mention.edges()
#         if g_mention.ep.weight[edge] < mention_threshold
#     ]

#     for edge in mention_edges_to_remove:
#         g_mention.remove_edge(edge)

#     logger.info(
#         (
#             f"Created User Mention Network for '{channel}'\n"
#             f"Used edge threshold (mention): {mention_threshold}\n"
#             f"Number of nodes: {g_mention.num_vertices()}\n"
#             f"Number of edges: {g_mention.num_edges()}\n"
#         )
#     )

#     networks.save_gt(g_mention, f"../output/comments_{channel}_mention_network")
#     all_m_wels.append(edges)


# # concatenate edges
# # all_b_wel = pd.concat(all_b_wels)
# # all_b_wel.to_csv(
# #     "../output/comments_topic_entity_all_weighted_edgelists.csv", index=False
# # )

# all_m_wel = pd.concat(all_m_wels)
# all_m_wel.to_csv(
#     "../output/comments_mentioned_users_all_weighted_edgelists.csv", index=False
# )
