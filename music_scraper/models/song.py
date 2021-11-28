from dataclasses import dataclass
from typing import List

from music_scraper.models.spotify_album_tracks import SpotifyAlbumTrack


@dataclass
class Song:
    title: str
    artists: List[str]
    spotify_album_id: str
    spotify_id: str

    def __str__(self) -> str:
        artists = ", ".join(self.artists)
        return f"{self.title} - {artists}"

    @classmethod
    def from_spotify_track(
        cls,
        track: SpotifyAlbumTrack,
        spotify_album_id: str,
    ):
        artists = [a.name for a in track.artists]
        return cls(track.name, artists, spotify_album_id, track.id)
