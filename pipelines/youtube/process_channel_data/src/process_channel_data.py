import json
from pathlib import Path

import pandas as pd
import yaml

import icsspy
import icsspy.cleaners as clean
import icsspy.utils as utils

logger = icsspy.initialize_logger()

with open("process_channel_data.yaml", "r") as file:
    task_config = yaml.safe_load(file)

video_metadata_keep_keys = task_config.get("video_metadata_keep_keys", {})
remove_substrings_dict = task_config.get("remove_substrings", {})


fpaths_fnames = utils.get_fpaths_and_fnames("../input", ftype="json")

channel_dfs = []
for fpath, fname in fpaths_fnames:
    logger.info(f"Processing {fname}")

    with open(fpath, "r") as f:
        data = json.load(f)
    df = pd.json_normalize(data)

    texts = clean.merge_title_and_description_strings(
        df, "snippet.title", "snippet.description"
    )

    processed_texts, urls = [], []
    for text in texts:
        text = text.replace("\n", "")
        text = clean.remove_text_in_brackets(text)

        text, urls_in_text = clean.process_urls(text)
        urls.append(urls_in_text)

        remove_substrings = remove_substrings_dict.get(fname, [])
        if len(remove_substrings) >= 1:
            text = clean.remove_substrings(text, remove_substrings)
        processed_texts.append(text)

    video_metadata_usecols = [c for c in df.columns if c in video_metadata_keep_keys]
    df = df[video_metadata_usecols]

    df["processed_text"] = processed_texts
    df["video_id"] = df["id"]
    df["channel"] = df["snippet.channelTitle"]

    channel_dfs.append(df)


df = pd.concat(channel_dfs)
output_path = Path("../output/channels_processed.csv")
df.to_csv(output_path, index=False)
logger.info("Finished processing all channel data")
