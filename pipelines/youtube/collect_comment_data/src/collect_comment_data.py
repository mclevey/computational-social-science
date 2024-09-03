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

with open("collect_comment_data.yaml", "r") as file:
    task_config = yaml.safe_load(file)

collect_comment_nans = task_config.get("attempt_to_collect_when_comments_unknown")
no_redownloading = task_config.get("no_redownloading")


df = pd.read_csv("../input/channels_processed.csv")

# reduce api calls; which videos have comments to request?
probably_no_public_comments = df[df["statistics.commentCount"].isna()]["id"].tolist()
no_public_comments = df[df["statistics.commentCount"] == 0]["id"].tolist()
has_public_comments = df[df["statistics.commentCount"] > 0]["id"].tolist()

logger.info(
    (
        f"Comment Counts\n"
        f"{len(has_public_comments):,} videos with comments\n"
        f"{len(no_public_comments):,} videos with no comments\n"
        f"{len(probably_no_public_comments):,} videos missing comment data\n"
    )
)

# Do not re-download videos that were previously downloaded (API quotas, etc.)
if no_redownloading is True:
    try:
        already_downloaded = pd.read_csv("../output/comments.csv")
        already_downloaded = already_downloaded["video_id"].unique().tolist()
        has_public_comments = [
            video
            for video in has_public_comments
            if video not in set(already_downloaded)
        ]
    except (FileNotFoundError, pd.errors.EmptyDataError):
        already_downloaded = []


logger.info(
    (
        f"{len(already_downloaded)} videos already collected. "
        f"{len(has_public_comments):,} videos to download.\n"
    )
)

if collect_comment_nans is True:
    collect = has_public_comments + probably_no_public_comments
    collect_n = len(collect)
    logger.info(
        f"Attempting to collect data for an additional {len(collect_n):,} videos"
    )
else:
    collect = has_public_comments
    collect_n = len(collect)
    logger.info(f"Attempting to collect data for {collect_n:,} videos.\n")

all_comments = yt.collect_comments_for_videos(
    YOUTUBE_API, collect, "../output/comments.csv", overwrite=True
)
