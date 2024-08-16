import pandas as pd
import yaml

import icsspy
import icsspy.utils as utils
import icsspy.youtube as yt

logger = icsspy.initialize_logger()

with open("../input/config.yaml", "r") as file:
    config = yaml.safe_load(file)

CHANNELS = config.get("channels", [])
KEY_NAMES = config.get("list_youtube_api_key_names", "YOUTUBE_API_KEY")
API_KEYS = utils.load_api_key_list(KEY_NAMES)
YOUTUBE_API = yt.YouTubeAPI(API_KEYS)


channel_ids = {}
for channel in CHANNELS:
    channel_id = yt.get_channel_id(YOUTUBE_API, channel)
    if channel_id:
        channel_ids[channel] = channel_id
    else:
        logger.info(f"Channel ID not found for '{channel}'")

logger.info(f"Retrieved IDs for:\n{channel_ids}")

ids = pd.DataFrame(list(channel_ids.items()), columns=["Channel", "ChannelID"])
ids.to_csv("../output/channel_ids.csv", index=False)
logger.info(f'Collected channel IDs for: \n{", ".join([c for c in CHANNELS])}\n')
print(ids)
