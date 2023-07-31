import datetime
import os

import isodate
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = ''
        self.url = ''
        self.print_info()

    def print_info(self):
        """Выводит в консоль информацию о плейлисте."""
        self.pl = self.youtube.playlists().list(id=self.playlist_id, part='contentDetails,snippet',
                                                maxResults=50, ).execute()
        video_response = self.pl['items'][0]
        self.title: str = video_response['snippet']['title']
        self.url: str = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def total_duration(self):
        video_ids = []
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        for video in playlist_videos['items']:
            video_ids.append(video['contentDetails']['videoId'])
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(video_ids)
                                                         ).execute()
        duration_total = datetime.timedelta()
        for video in self.video_response['items']:
            duration_isodate = video['contentDetails']['duration']
            duration = isodate.parse_duration(duration_isodate)
            duration_total += duration
        return duration_total

    def show_best_video(self):
        video_id = []
        video_likes = []
        video_response = self.video_response
        for video in video_response['items']:
            video_id.append(video['id'])
            video_likes.append(int(video['statistics']['likeCount']))
        best_video = video_id[video_likes.index(max(video_likes))]
        return f"https://youtu.be/{best_video}"
