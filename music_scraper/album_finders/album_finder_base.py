from abc import ABC, abstractmethod
from typing import Iterator

from music_scraper.models import Album


class AlbumFinderBase(ABC):
    @property
    @abstractmethod
    def get_url(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_albums(self) -> Iterator[Album]:
        raise NotImplementedError
