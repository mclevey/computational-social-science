import pandas as pd
import yaml

import icsspy
import icsspy.text as text

logger = icsspy.initialize_logger()

with open("label_channel_topics.yaml", "r") as file:
    task_config = yaml.safe_load(file)

df = pd.read_csv("../input/channels_processed.csv")
df["processed_text"] = df["processed_text"].astype(str)

all_text_topic_dfs = []
all_topic_info_dfs = []

channel_map = {
    "PyData": "PyData",
    "EuroPython Conference": "EuroPythonConference",
    "Data & Society Research Institute": "datasocietyresearchinstitu1085",
    "Microsoft Research": "MicrosoftResearch",
    "Talks at Google": "talksatgoogle",
}

for channel_name, group_df in df.groupby("channel"):
    default_params = task_config.get("DEFAULT_PARAMS", {})
    channel = channel_map[channel_name]

    # get channel-specific parameters or use default
    channel_config = task_config.get(channel, default_params)
    tm_params = channel_config.get("topic_model", default_params["topic_model"])
    rm_params = channel_config.get(
        "representation_model", default_params["representation_model"]
    )

    # topic model parameters (defaults above)
    umap_n_neighbors = tm_params.get("umap_n_neighbors")
    umap_n_components = tm_params.get("umap_n_components")
    hdbscan_min_cluster_size = tm_params.get("hdbscan_min_cluster_size")
    hdbscan_min_samples = tm_params.get("hdbscan_min_samples")
    mmr_model_diversity = tm_params.get("mmr_model_diversity")

    # representation model parameters (defaults above)
    vectorizer_min_df = rm_params.get("vectorizer_min_df")
    vectorizer_max_df = rm_params.get("vectorizer_max_df")
    ngram_upper_limit = rm_params.get("ngram_upper_limit")
    top_n_words = rm_params.get("top_n_words")

    text_topic_df, topic_info, topic_model = text.label_topics(
        group_df,
        textcol="processed_text",
        umap_n_neighbors=umap_n_neighbors,
        umap_n_components=umap_n_components,
        hdbscan_min_cluster_size=hdbscan_min_cluster_size,
        hdbscan_min_samples=hdbscan_min_samples,
        mmr_model_diversity=mmr_model_diversity,
        vectorizer_min_df=vectorizer_min_df,
        vectorizer_max_df=vectorizer_max_df,
        ngram_upper_limit=ngram_upper_limit,
        top_n_words=top_n_words,
    )

    text_topic_df["channel"] = channel
    topic_info["channel"] = channel

    all_text_topic_dfs.append(text_topic_df)
    all_topic_info_dfs.append(topic_info)

    print(f"\n{channel} Topics")
    text.preview_topics(text_topic_df, topic_info)
    print("\n")

final_text_topic_df = pd.concat(all_text_topic_dfs, ignore_index=True)
final_text_topic_df.to_csv("../output/channels_topics.csv", index=False)

final_topic_info_df = pd.concat(all_topic_info_dfs, ignore_index=True)
final_topic_info_df.to_csv("../output/channels_topic_info.csv", index=False)
logger.info("Finished labelling topics")
