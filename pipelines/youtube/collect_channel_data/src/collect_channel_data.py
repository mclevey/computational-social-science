import pandas as pd
import yaml

import icsspy
import icsspy.utils as utils
import icsspy.youtube as yt

logger = icsspy.initialize_logger()

with open("../input/config.yaml", "r") as file:
    config = yaml.safe_load(file)

KEY_NAMES = config.get("list_youtube_api_key_names", "YOUTUBE_API_KEY")
API_KEYS = utils.load_api_key_list(KEY_NAMES)
YOUTUBE_API = yt.YouTubeAPI(API_KEYS)

channels = pd.read_csv("../input/channel_ids.csv")
cnames = channels["Channel"].tolist()
cids = channels["ChannelID"].tolist()


for cname, cid in zip(cnames, cids):
    logger.info(f"Collecting data for {cname} (ID: {cid})")

    video_ids = yt.get_channel_video_ids(YOUTUBE_API, cid)
    if not video_ids:
        logger.warning(f"No videos found for {cname} (ID: {cid})")
        continue

    video_details = yt.get_channel_video_data(YOUTUBE_API, video_ids)

    output_file = f"../output/{cname}.json"
    utils.save_json(video_details, output_file)

    logger.info(f"Saved data for {len(video_details)} videos to {output_file}.")
