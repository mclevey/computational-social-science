import pandas as pd
import yaml
from tabulate import tabulate

import icsspy

logger = icsspy.initialize_logger()

channels = pd.read_csv("../input/channels_processed.csv")[["video_id", "channel"]]
comments = pd.read_csv("../input/comments_processed.csv")[["comment_id", "channel"]]

# Calculate video counts per channel
video_counts = channels.groupby("channel").size().reset_index(name="videos")
video_counts["videos"] = video_counts["videos"].apply(lambda x: f"{x:,}")

# Calculate comment counts per channel
comment_counts = comments.groupby("channel").size().reset_index(name="comments")
comment_counts["comments"] = comment_counts["comments"].apply(lambda x: f"{x:,}")

# Merge video and comment counts
counts = pd.merge(video_counts, comment_counts, on="channel", how="outer")
counts.columns = ["Channel", "Video Count", "Comment Count"]
counts["Comment Count"] = counts["Comment Count"].fillna("Comments Disabled")  # D&S

# LANGUAGES
with open("language_map.yaml", "r") as file:
    language_map = yaml.safe_load(file)

# Load and process predicted language data
languages = pd.read_csv("../input/comments_predicted_language.csv")
languages["predicted_language"] = languages["predicted_language"].map(language_map)
languages["is_en"] = languages["predicted_language"] == "English"

# Merge comments with their predicted languages
merge = pd.merge(comments, languages, on="comment_id", how="left")
merge["is_en"] = merge["is_en"].fillna(False)
# ^ Assume unknown languages are not English (since English is known)

# Calculate total and English comments per channel
total_comments = merge.groupby("channel").size().reset_index(name="total_comments")
english_comments_grouped = merge[merge["is_en"]].groupby("channel")
english_comments = english_comments_grouped.size().reset_index(name="en_comments")
merge["is_en"] = merge["is_en"].astype(bool)

# Merge total and English comment counts
comment_counts = pd.merge(total_comments, english_comments, on="channel", how="left")
comment_counts["en_comments"] = comment_counts["en_comments"].fillna(0)

# Calculate percentage of English comments
comment_counts["percentage"] = (
    comment_counts["en_comments"] / comment_counts["total_comments"]
) * 100

comment_counts["percentage"] = comment_counts["percentage"].round(2)

# Merge video counts with comment statistics
merge = pd.merge(video_counts, comment_counts, on="channel", how="outer")
merge.fillna(0, inplace=True)

# Format numeric columns with commas
merge["total_comments"] = merge["total_comments"].astype(int).apply(lambda x: f"{x:,}")
merge["en_comments"] = merge["en_comments"].astype(int).apply(lambda x: f"{x:,}")

merge.columns = [
    "Channel",
    "Video Count",
    "Comment Count",
    "No. English Comments",
    "Percentage English",
]

# Generate markdown table
counts_table = tabulate(merge, headers="keys", tablefmt="pipe", showindex=False)
with open("../output/counts_table.md", "w") as f:
    f.write(counts_table)

# Log the output and print the table
logger.info("Wrote channel and comment data to markdown tables\n")
print(counts_table)
