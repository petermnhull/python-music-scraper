from pydantic import BaseModel
from typing import List

from music_scraper.models.spotify_album_search import SpotifyArtist


class SpotifyAlbumTrack(BaseModel):
    id: str
    name: str
    artists: List[SpotifyArtist]


class SpotifyAlbumTracksResult(BaseModel):
    items: List[SpotifyAlbumTrack]
    total: int
