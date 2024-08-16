import pandas as pd

import icsspy
import icsspy.text as text

logger = icsspy.initialize_logger()

top_sent = {
    "topics": "../input/comments_topics.csv",
    "sentiment": "../input/comments_sentiment.csv",
}

comment_dfs = []
for k, fpath in top_sent.items():
    df = pd.read_csv(fpath)
    df[f"processed_text_{k}"] = df["processed_text"]
    df = df.drop(columns=["processed_text"])
    comment_dfs.append(df)

# perform iterative merges of dfs in comment_dfs
merged = comment_dfs[0]
for df in comment_dfs[1:]:
    merged = pd.merge(merged, df, on="comment_id", how="outer")

merged = merged.dropna()
merged["processed_text"] = merged["processed_text_sentiment"]

merged = merged.drop(
    columns=[
        "channel_x",  # duplicated
        "channel_y",  # duplicated
    ]
)

logger.info("Finished merging comments")
# print(merged.info())

# NOW ADD ENTITIES!
entities = pd.read_csv("../input/comments_entities.csv")
ent_keep_list = ["product-software"]

entities = text.filter_entities(entities, "label", ent_keep_list, "score", 0.8)
entities = text.group_entities(entities, "comment_id", "span", "score")

entities.rename(
    columns={"spans_list": "entities_list", "scores_list": "entities_scores_list"},
    inplace=True,
)

merged = pd.merge(merged, entities, on="comment_id", how="outer")
merged.to_csv("../output/comments_merged_labelled_text.csv", index=False)
print(merged.columns)
