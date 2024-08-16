import pandas as pd
import yaml

import icsspy
import icsspy.text as text

logger = icsspy.initialize_logger()

with open("label_channel_topics.yaml", "r") as file:
    task_config = yaml.safe_load(file)


bertopic_params = task_config.get("bertopic")
umap_n_neighbors = bertopic_params.get("umap_n_neighbors", 15)
umap_n_components = bertopic_params.get("umap_n_components", 5)
hdbscan_min_cluster_size = bertopic_params.get("hdbscan_min_cluster_size", 10)
hdbscan_min_samples = bertopic_params.get("hdbscan_min_samples", 5)
mmr_model_diversity = bertopic_params.get("mmr_model_diversity", 0.3)

representation_params = task_config.get("representation")
vectorizer_min_df = representation_params.get("vectorizer_min_df", 15)
vectorizer_max_df = representation_params.get("vectorizer_max_df", 5)
ngram_upper_limit = representation_params.get("ngram_upper_limit", 10)
hdbscan_min_samples = representation_params.get("hdbscan_min_samples", 5)
top_n_words = representation_params.get("top_n_words", 0.3)


df = pd.read_csv("../input/channels_processed.csv")
df["processed_text"] = df["processed_text"].astype(str)

all_text_topic_dfs = []
all_topic_info_dfs = []

for channel, group_df in df.groupby("channel"):
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
