# import pickle

# import graph_tool.all as gt
# import pandas as pd
# import yaml

# import icsspy
# import icsspy.networks as networks

# logger = icsspy.initialize_logger()


# with open("model_networks.yaml", "r") as file:
#     task_config = yaml.safe_load(file)

# two_mode_channel_networks = task_config.get("two_mode_channel_networks")

# all_block_data = []
# for netname, netpath in two_mode_channel_networks.items():
#     g = networks.load_gt(netpath)
#     if g.num_vertices() > 0 and g.num_edges() > 0:
#         try:
#             # the bipartite property has to be in vertex_properties
#             bipartite = g.vertex_properties["vtype"]

#             # vertex type counts
#             num_type_0 = sum(1 for v in g.vertices() if bipartite[v] == 0)
#             num_type_1 = sum(1 for v in g.vertices() if bipartite[v] == 1)
#             logger.info(
#                 (
#                     f"Node Types for '{netname}' Network\n"
#                     f"Type 0: {num_type_0}\nType 1: {num_type_1}\n"
#                 )
#             )

#             # BIPARTITE HBSBM

#             # blockmodel = networks.create_blockmodel(g, bip=bipartite)
#             blockmodel, block_data = networks.fit_hbsbm(
#                 g, bip=bipartite, refine="basic", vertex_property_key="name"
#             )
#             # gd = networks.get_graph_data(blockmodel)
#             # gd["netname"] = netname
#             block_data["netname"] = netname
#             # all_block_data.append(gd)
#             all_block_data.append(block_data)

#             with open(f"../output/{netname}_bipartite_blockstate.pkl", "wb") as f:
#                 pickle.dump(blockmodel, f)

#             gt.draw_hierarchy(
#                 blockmodel,
#                 layout="bipartite",
#                 bip_aspect=1.0,
#                 output=f"../output/{netname}_bipartite_blockmodel.pdf",
#                 output_size=(3000, 3000),
#                 bg_color=[1, 1, 1, 1],
#                 vprops={
#                     "text": g.vp["name"],
#                     "text_position": 0,
#                     "text_color": "black",
#                 },
#             )

#             logger.info(f"Estimated a Bipartite HBSBM for '{netname}'\n")
#         except KeyError as e:
#             logger.error(f"KeyError for '{netname}': {e}")
#         except Exception as e:
#             logger.error(f"An error occurred for '{netname}': {e}")

# if all_block_data:
#     all_block_data = pd.concat(all_block_data)
#     all_block_data.to_csv(
#         "../output/bipartite_topic_entity_all_block_data.csv", index=False
#     )
# else:
#     print("No graph data to concatenate.")
