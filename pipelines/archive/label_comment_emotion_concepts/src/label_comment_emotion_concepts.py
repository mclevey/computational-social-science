import pandas as pd

import icsspy
import icsspy.text as t

logger = icsspy.initialize_logger()

df = pd.read_csv("../input/comments_processed.csv")
df["processed_text"] = df["processed_text"].astype(str)

model = "cardiffnlp/twitter-roberta-base-emotion-multilabel-latest"

all_emotion_concept_dfs = []

for channel, group_df in df.groupby("channel"):
    emotion_concepts = t.label_emotion_concepts(
        model=model, df=group_df, textcol="processed_text", idcol="comment_id"
    )

    emotion_concepts["channel"] = channel

    all_emotion_concept_dfs.append(emotion_concepts)

final_emotion_concepts_df = pd.concat(all_emotion_concept_dfs, ignore_index=True)
final_emotion_concepts_df.to_csv("../output/comments_emotion_concepts.csv", index=False)
logger.info("Finished labelling emotion concepts in comments data")
print(final_emotion_concepts_df.sample(10))
