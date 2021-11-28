from pydantic import BaseModel
from typing import List

from music_scraper.models.album import Album
from music_scraper.models.utils import normalise_string


class SpotifyArtist(BaseModel):
    name: str


class SpotifyAlbum(BaseModel):
    id: str
    artists: List[SpotifyArtist]

    def album_matches(self, album: Album) -> bool:
        """
        Returns whether an album object matches the album in Spotify's response.
        Simply checks whether there is an overlap in artists for now.
        """
        artists = set(normalise_string(a.name) for a in self.artists)
        artists_to_find = set(normalise_string(a) for a in album.artists)
        matched = artists.intersection(artists_to_find)
        return bool(matched)


class SpotifyAlbums(BaseModel):
    items: List[SpotifyAlbum]


class SpotifyAlbumSearchResult(BaseModel):
    albums: SpotifyAlbums

    def find_matching_album_id(self, album: Album) -> str:
        for spotify_album in self.albums.items:
            if spotify_album.album_matches(album):
                return spotify_album.id
        return ""
