import pandas as pd
import yaml

import icsspy
import icsspy.text as text

logger = icsspy.initialize_logger()

with open("merge_labelled_channel_data.yaml", "r") as file:
    task_config = yaml.safe_load(file)

entities = pd.read_csv("../input/channels_entities.csv")
sentiment = pd.read_csv("../input/channels_sentiment.csv")
topics = pd.read_csv("../input/channels_topics.csv")
topic_info = pd.read_csv("../input/channels_topic_info.csv")

# align column names for merging (fix this upstream later...)
topic_info.rename(columns={"Topic": "topic"}, inplace=True)

# grouped by channel
# FIX THESE COLUMN NAMES UPSTREAM!
entities_grouped = entities.groupby("channel")
# print("entities_grouped", entities_grouped.groups.keys())

sentiment_grouped = sentiment.groupby("channel")
# print("sentiment_grouped", sentiment_grouped.groups.keys())

# FIX THESE COLUMN NAMES UPSTREAM!
topics["channel"] = topics["channel"].replace(
    {
        "PyData": "PyData",
        "EuroPythonConference": "EuroPython Conference",
        "datasocietyresearchinstitu1085": "Data & Society Research Institute",
        "MicrosoftResearch": "Microsoft Research",
        "talksatgoogle": "Talks at Google",
    }
)
topics_grouped = topics.groupby("channel")
# print("topics_grouped", topics_grouped.groups.keys())

# FIX THESE COLUMN NAMES UPSTREAM!
topic_info["channel"] = topic_info["channel"].replace(
    {
        "PyData": "PyData",
        "EuroPythonConference": "EuroPython Conference",
        "datasocietyresearchinstitu1085": "Data & Society Research Institute",
        "MicrosoftResearch": "Microsoft Research",
        "talksatgoogle": "Talks at Google",
    }
)
topic_info_grouped = topic_info.groupby("channel")
# print("topic_info_grouped", topic_info_grouped.groups.keys())

channel_map = {
    "PyData": "PyData",
    "EuroPython Conference": "EuroPythonConference",
    "Data & Society Research Institute": "datasocietyresearchinstitu1085",
    "Microsoft Research": "MicrosoftResearch",
    "Talks at Google": "talksatgoogle",
}

merged_results = []
for channel_name, group_df in entities_grouped:
    channel = channel_map.get(channel_name)
    if channel is None:
        logger.warning(f"Channel name {channel_name} not found in channel_map.")
        continue

    # print(channel, channel_name)

    entity_group = entities_grouped.get_group(channel_name)
    sentiment_group = sentiment_grouped.get_group(channel_name)
    topic_group = topics_grouped.get_group(channel_name)
    topic_info_group = topic_info_grouped.get_group(channel_name)

    # process entities (maybe do this downstream?)
    # ent_keep_list = task_config.get("entity_types", ['product-software'])
    # entity_group = text.filter_entities(
    #     entity_group,
    #     "label",
    #     ent_keep_list,
    #     "score",
    #     task_config.get("entity_score_threshold", 0.7),
    # )
    entity_group = text.group_entities(entity_group, "video_id", "span", "score")
    entity_group.rename(
        columns={"spans_list": "entities_list", "scores_list": "entities_scores_list"},
        inplace=True,
    )

    # merge the groups on 'video_id'
    merged_group = pd.merge(entity_group, topic_group, on="video_id", how="outer")
    # add in the descriptive topics via the topic info df merged on "topic"
    merged_group = pd.merge(merged_group, topic_info_group, on="topic")  # topic info
    # sentiment group (will I need to clean up channels again here?)
    merged_group = pd.merge(merged_group, sentiment_group, on="video_id", how="outer")

    # handle possible column name conflicts
    if "channel_x" in merged_group.columns and "channel_y" in merged_group.columns:
        merged_group["channel"] = channel
        merged_group.drop(columns=["channel_x", "channel_y"], inplace=True)

    merged_results.append(merged_group)

merged = pd.concat(merged_results, ignore_index=True)
merged.to_csv("../output/channels_merged_labelled_text.csv", index=False)
logger.info("Finished merging labelled channel data")
print(merged.columns)
