from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Album:
    title: str
    artists: List[str]
    release_type: str
    found_at: datetime

    def __str__(self) -> str:
        artists = ", ".join(self.artists)
        return f"{self.title} - {artists}"
