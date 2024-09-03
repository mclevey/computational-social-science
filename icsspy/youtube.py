import csv
import html
import logging
import time
from typing import Any, Dict, List, Optional

from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError
from tqdm import tqdm


class YouTubeAPI:
    def __init__(self, api_keys: List[str]) -> None:
        self.api_keys = api_keys
        self.key_index = 0
        self.service = self.build_service()

    def build_service(self) -> Resource:
        return build(
            "youtube",
            "v3",
            developerKey=self.api_keys[self.key_index],
            cache_discovery=False,
        )

    def switch_key(self) -> None:
        self.key_index = (self.key_index + 1) % len(self.api_keys)
        self.service = self.build_service()

    def execute_request(self, request: Any) -> Any:
        wait_time = 1  # initial wait time in seconds
        max_retries = 5  # maximum number of retries

        for _ in range(max_retries):
            try:
                response = request.execute()
                return response
            except HttpError as e:
                if e.resp.status in [403, 429]:  # Rate limit exceeded
                    logging.info(
                        (
                            "Rate limit exceeded for API key: "
                            f"{self.api_keys[self.key_index]}. Switching keys."
                        )
                    )
                    self.switch_key()
                    print(f"Waiting for {wait_time} seconds before retrying...")
                    time.sleep(wait_time)
                    wait_time *= 2  # Exponential backoff
                else:
                    raise e

        raise Exception("Max retries exceeded")


def get_channel_id_by_username(youtube_api: YouTubeAPI, username: str) -> Optional[str]:
    """Get the channel ID by username."""
    try:
        request = youtube_api.service.channels().list(part="id", forUsername=username)
        response = youtube_api.execute_request(request)

        if "items" in response and len(response["items"]) > 0:
            return response["items"][0]["id"]
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_channel_id_by_custom_url(
    youtube_api: YouTubeAPI, custom_url: str
) -> Optional[str]:
    """Get the channel ID by custom URL."""
    try:
        request = youtube_api.service.search().list(
            part="snippet", q=custom_url, type="channel"
        )
        response = youtube_api.execute_request(request)

        if "items" in response and len(response["items"]) > 0:
            return response["items"][0]["snippet"]["channelId"]
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_channel_id(youtube_api: YouTubeAPI, channel: str) -> Optional[str]:
    """
    Get the channel ID given a channel name or custom URL.
    """
    # First, try to get the channel ID by custom URL
    cid = get_channel_id_by_custom_url(youtube_api, channel)
    if cid is not None:
        return cid
    # If not found, try to get the channel ID by username
    return get_channel_id_by_username(youtube_api, channel)


def get_channel_video_ids(youtube_api: YouTubeAPI, channel_id: str) -> List[str]:
    """Retrieve all video IDs from the channel's uploads playlist."""
    try:
        request = youtube_api.service.channels().list(
            part="contentDetails", id=channel_id
        )
        response = youtube_api.execute_request(request)

        if "items" not in response or len(response["items"]) == 0:
            logging.error(f"No items found for channel ID: {channel_id}")
            return []

        uploads_playlist_id = response["items"][0]["contentDetails"][
            "relatedPlaylists"
        ]["uploads"]

        # Retrieve all videos in the uploads playlist
        videos: List[str] = []
        next_page_token: Optional[str] = None
        while True:
            playlist_request = youtube_api.service.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token,
            )
            playlist_response = youtube_api.execute_request(playlist_request)

            for item in playlist_response.get("items", []):
                video_id = item["snippet"]["resourceId"]["videoId"]
                videos.append(video_id)

            next_page_token = playlist_response.get("nextPageToken")
            if next_page_token is None:
                break

        return videos
    except Exception as e:
        logging.error(
            f"An error occurred while fetching videos for channel ID {channel_id}: {e}"
        )
        return []


def get_channel_video_data(
    youtube_api: YouTubeAPI, video_ids: List[str]
) -> List[Dict[str, Any]]:
    """Retrieve detailed information for each video."""
    video_details: List[Dict[str, Any]] = []
    for i in range(0, len(video_ids), 50):
        try:
            request = youtube_api.service.videos().list(
                part=(
                    "snippet,contentDetails,statistics,status,topicDetails,"
                    "recordingDetails,player,liveStreamingDetails"
                ),
                id=",".join(video_ids[i : i + 50]),
            )
            response = youtube_api.execute_request(request)

            for item in response.get("items", []):
                video_details.append(item)
        except Exception as e:
            logging.error(f"An error occurred while fetching video details: {e}")

    return video_details


def collect_comments_for_videos(
    youtube_api: YouTubeAPI,
    video_ids: List[str],
    filename: str,
    overwrite: bool = False,
) -> None:
    fieldnames = [
        "video_id",
        "comment_id",
        "text",
        "author",
        "author_channel_url",
        "like_count",
        "published_at",
        "updated_at",
    ]

    # If overwrite is True, open the file in write mode and write the header
    if overwrite:
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    # Open the file in append mode and write video data to disk in real-time
    with open(filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for video_id in tqdm(video_ids, desc="Videos", unit="video"):
            try:
                comments = get_video_comments(
                    youtube_api=youtube_api, video_id=video_id
                )
                if comments is not None:
                    for comment in comments:
                        # Add the video_id to each comment dictionary
                        comment["video_id"] = video_id
                        # Decode HTML entities in the text field
                        comment["text"] = html.unescape(comment["text"])
                        writer.writerow(comment)
            except HttpError as e:
                error_details = e.error_details[0] if e.error_details else {}
                reason = error_details.get("reason")
                if reason in ["quotaExceeded", "userRateLimitExceeded"]:
                    logging.error(
                        "Quota exceeded or rate limit reached. Stopping execution."
                    )
                    break
                else:
                    logging.error(
                        (
                            "An error occurred while fetching comments for"
                            f"{video_id}: {e}"
                        )
                    )


def get_video_comments(
    youtube_api: YouTubeAPI, video_id: str
) -> Optional[List[Dict[str, Any]]]:
    """Retrieve comments for a given video ID."""
    try:
        request = youtube_api.service.commentThreads().list(
            part="snippet,replies", videoId=video_id, maxResults=100
        )
        comments: List[Dict[str, Any]] = []
        while request:
            response = youtube_api.execute_request(request)
            for item in response.get("items", []):
                comment_data = {
                    "comment_id": item["id"],
                    "text": item["snippet"]["topLevelComment"]["snippet"][
                        "textDisplay"
                    ],
                    "author": item["snippet"]["topLevelComment"]["snippet"][
                        "authorDisplayName"
                    ],
                    "author_channel_url": item["snippet"]["topLevelComment"]["snippet"][
                        "authorChannelUrl"
                    ],
                    "like_count": item["snippet"]["topLevelComment"]["snippet"][
                        "likeCount"
                    ],
                    "published_at": item["snippet"]["topLevelComment"]["snippet"][
                        "publishedAt"
                    ],
                    "updated_at": item["snippet"]["topLevelComment"]["snippet"][
                        "updatedAt"
                    ],
                }
                comments.append(comment_data)
                # Check for replies
                if "replies" in item:
                    for reply in item["replies"]["comments"]:
                        reply_data = {
                            "comment_id": reply["id"],
                            "text": reply["snippet"]["textDisplay"],
                            "author": reply["snippet"]["authorDisplayName"],
                            "author_channel_url": reply["snippet"]["authorChannelUrl"],
                            "like_count": reply["snippet"]["likeCount"],
                            "published_at": reply["snippet"]["publishedAt"],
                            "updated_at": reply["snippet"]["updatedAt"],
                        }
                        comments.append(reply_data)
            request = youtube_api.service.commentThreads().list_next(request, response)
        return comments
    except HttpError as e:
        error_details = e.error_details[0] if e.error_details else {}
        reason = error_details.get("reason")
        if reason == "commentsDisabled":
            logging.warning(f" Comments are disabled for video {video_id}")
        else:
            logging.error(
                (" An error occurred while fetching comments for" f"{video_id}: {e}")
            )
        return None
