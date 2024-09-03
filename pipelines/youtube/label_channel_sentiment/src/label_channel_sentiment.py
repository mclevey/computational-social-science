import pandas as pd

import icsspy
import icsspy.text as t

logger = icsspy.initialize_logger()

df = pd.read_csv("../input/channels_processed.csv")

df["processed_text"] = df["processed_text"].astype(str)

model = "cardiffnlp/twitter-roberta-base-sentiment-latest"

all_sentiment_dfs = []

for channel, group_df in df.groupby("channel"):
    sentiment = t.label_sentiment(
        model=model, df=group_df, textcol="processed_text", idcol="video_id"
    )

    sentiment["channel"] = channel
    all_sentiment_dfs.append(sentiment)

final_sentiment_df = pd.concat(all_sentiment_dfs, ignore_index=True)
final_sentiment_df.to_csv("../output/channels_sentiment.csv", index=False)
logger.info("Finished labelling sentiment in channels data")
print(final_sentiment_df.sample(30))
