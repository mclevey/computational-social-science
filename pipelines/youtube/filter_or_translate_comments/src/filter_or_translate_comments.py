import pandas as pd

import icsspy

logger = icsspy.initialize_logger()

comments = pd.read_csv("../input/comments_processed.csv")
comments_predlang = pd.read_csv("../input/comments_predicted_language.csv")

merged_comments = comments.merge(comments_predlang, on="comment_id", how="left")
print(merged_comments.value_counts("predicted_language"))

english_comments = merged_comments.loc[merged_comments["predicted_language"] == "en"]
english_comments = merged_comments.loc[merged_comments["confidence_score"] > 0.9]

english_comments.to_csv("../output/comments_processed_english.csv", index=False)
logger.info("Filtered comments to English only with confidence score > 0.9\n")
