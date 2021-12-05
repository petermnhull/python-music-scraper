import json
import datetime

from music_scraper.models import Album
from music_scraper.models.spotify_album_search import (
    SpotifyAlbumSearchResult,
    SpotifyAlbums,
    SpotifyAlbum,
    SpotifyArtist,
)

MOCK_ALBUM_ONE = Album(
    title="good song",
    artists=["Firstname Lastname", "Random Collaborator"],
    release_type="album",
    found_at=datetime.datetime(2021, 1, 1, 1, 1),
)


MOCK_ALBUM_TWO = Album(
    title="bad song",
    artists=["Firstname Lastname"],
    release_type="ep",
    found_at=datetime.datetime(2021, 1, 1, 1, 1),
)


MOCK_ALBUM_SEARCH_MAP = {
    "albums": {"items": [{"id": "123abc", "artists": [{"name": "random collaborator"}]}]}
}

MOCK_SEARCH_MODEL_ARTIST = SpotifyArtist(name="random collaborator")
MOCK_SEARCH_MODEL_ALBUM = SpotifyAlbum(id="123abc", artists=[MOCK_SEARCH_MODEL_ARTIST])
MOCK_SEARCH_MODEL_ALBUMS = SpotifyAlbums(items=[MOCK_SEARCH_MODEL_ALBUM])
MOCK_SEARCH_MODEL_ALBUMS_RESULT = SpotifyAlbumSearchResult(albums=MOCK_SEARCH_MODEL_ALBUMS)


class MockResponse:
    def __init__(self, text: str, status_code: int):
        self.text = text
        self.status_code = status_code
        self.url = ""

    def json(self):
        return json.loads(self.text)
