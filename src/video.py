import os
from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video):
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.id_video = id_video
        self.video_title = ""
        self.view_count = 0
        self.like_count = 0
        self.comment_count = 0
        self.url = ""
        self.print_info()

    def print_info(self):
        """Выводит в консоль информацию о видео."""
        self.video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                id=self.id_video).execute()
        video_response = self.video['items'][0]
        self.video_title: str = video_response['snippet']['title']
        self.view_count: int = video_response['statistics']['viewCount']
        self.like_count: int = video_response['statistics']['likeCount']
        self.url: str = f'https://www.youtube.com/watch?v={self.id_video}'

    def __str__(self):
        return f'{self.video_title}'


class PLVideo(Video):
    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.id_playlist = id_playlist
