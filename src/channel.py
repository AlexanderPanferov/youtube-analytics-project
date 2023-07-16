import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = ""
        self.description = ""
        self.url = ""
        self.subscribers_count = 0
        self.video_count = 0
        self.views_count = 0
        self.print_info()

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, id):
        self.__channel_id = id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        data = self.channel['items'][0]
        self.title = data['snippet']['title']
        self.description = data['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscribers_count = int(data['statistics']['subscriberCount'])
        self.video_count = int(data['statistics']['videoCount'])
        self.views_count = int(data['statistics']['viewCount'])
        info = json.dumps(self.channel, indent=2, ensure_ascii=False)
        print(info)

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, filename):
        """Создаем словарь со значениями атрибутов. Записываем словарь в файл в формате JSON"""
        data = {
            "id": self.__channel_id,
            "name": self.title,
            "description": self.description,
            "link": self.url,
            "subscribers_count": self.subscribers_count,
            "video_count": self.video_count,
            "views_count": self.views_count
        }
        print(data)

        with open(filename, "w", encoding='utf-8') as f:
            json.dump(data, f)
