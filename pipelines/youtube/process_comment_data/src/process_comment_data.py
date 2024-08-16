import pandas as pd

import icsspy
import icsspy.cleaners as clean

logger = icsspy.initialize_logger()

comments = pd.read_csv("../input/comments.csv")

comments["processed_text"] = comments["text"].apply(clean.clean_comment_text)
comments.drop("text", axis=1, inplace=True)

# get channels for video-ids
channels = pd.read_csv("../input/channels_processed.csv")
channels = channels[["video_id", "channel"]]

comments = pd.merge(comments, channels, on="video_id", how="left")
print(comments.info())

comments.to_csv("../output/comments_processed.csv", index=False)
logger.info("Finished processing comment data")
