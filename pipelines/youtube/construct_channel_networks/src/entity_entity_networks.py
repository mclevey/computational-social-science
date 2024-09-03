import pandas as pd
import yaml

import icsspy
import icsspy.networks as networks
from icsspy.utils import strings_to_lists

logger = icsspy.initialize_logger()

with open("construct_channel_networks.yaml", "r") as file:
    task_config = yaml.safe_load(file)


global_edge_threshold = task_config.get("edge_threshold")

topic_info = pd.read_csv("../input/channels_topic_info.csv")

df = pd.read_csv("../input/channels_merged_labelled_text.csv")
df.dropna(subset=["entities_list"], inplace=True)
df["entities_list"] = strings_to_lists(df["entities_list"])


df_grouped = df.groupby("channel")
topic_info_grouped = topic_info.groupby("channel")

all_wels_context_video, all_wels_context_topic = [], []
for channel in df_grouped.groups.keys():
    entity_group = df_grouped.get_group(channel)

    topic_info_group = topic_info_grouped.get_group(channel).copy()
    topic_info_group.drop(columns="Count", inplace=True)

    # entity-entity within video titles and descriptions
    ee_wel_in_videos = networks.construct_cooccurrence_edgelist(
        df=entity_group, node_list_col="entities_list", context_group_col="video_id"
    )

    # entity-entity within topics
    ee_wel_in_topics = networks.construct_cooccurrence_edgelist(
        df=entity_group, node_list_col="entities_list", context_group_col="topic"
    )

    # threshold dataframes
    ee_wel_in_videos = ee_wel_in_videos[
        ee_wel_in_videos["count"] > global_edge_threshold
    ]
    ee_wel_in_topics = ee_wel_in_topics[
        ee_wel_in_topics["count"] > global_edge_threshold
    ]

    # append edgelists to all_wels lists
    ee_wel_in_videos["channel"] = channel
    all_wels_context_video.append(ee_wel_in_videos)

    ee_wel_in_topics["channel"] = channel
    all_wels_context_topic.append(ee_wel_in_topics)

    # construct final networks
    g_context_videos = networks.g_from_weighted_edgelist(ee_wel_in_videos)
    g_context_topics = networks.g_from_weighted_edgelist(ee_wel_in_topics)

    logger.info(
        (
            f"Created Entity-Entity Networks for '{channel}'\n"
            f"Used edge threshold: {global_edge_threshold}\n"
            f"Number of nodes in video context: {g_context_videos.num_vertices()}\n"
            f"Number of edges in video context: {g_context_videos.num_edges()}\n"
            f"Number of nodes in topic context: {g_context_topics.num_vertices()}\n"
            f"Number of edges in topic context: {g_context_topics.num_edges()}\n"
        )
    )

    output_network_context_video = (
        f"../output/channels_{channel}_entity_entity_[videos]"
    )
    networks.save_gt(g_context_videos, output_network_context_video)

    output_network_context_topic = (
        f"../output/channels_{channel}_entity_entity_[topics]"
    )
    networks.save_gt(g_context_topics, output_network_context_topic)


all_wels_context_videos = pd.concat(all_wels_context_video)
all_wels_context_videos.to_csv(
    "../output/channels_all_entity_entity_wels_[videos].csv", index=False
)
print(all_wels_context_videos.head(30))

all_wels_context_topics = pd.concat(all_wels_context_topic)
all_wels_context_topics.to_csv(
    "../output/channels_all_entity_entity_wels_[topics].csv", index=False
)
print(all_wels_context_topics.head(30))
