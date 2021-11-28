import pytest
from mock import MagicMock


from music_scraper.album_processor import AlbumProcessor
from music_scraper.album_finders import AlbumFinderBase
from music_scraper.clients import SpotifyClient
from music_scraper.models import Song
from tests.helpers import MOCK_ALBUM_ONE, MOCK_ALBUM_TWO


@pytest.fixture
def album_processor() -> AlbumProcessor:
    album_finder_one = MagicMock(spec=AlbumFinderBase)
    album_finder_one.get_url.return_value = "www.musicwebsite.com/albums"
    album_finder_one.get_albums.return_value = [MOCK_ALBUM_ONE]

    album_finder_two = MagicMock(spec=AlbumFinderBase)
    album_finder_two.get_url.return_value = "www.anothermusicwebsite.com/albums"
    album_finder_two.get_albums.return_value = [MOCK_ALBUM_TWO]

    album_finders = [album_finder_one, album_finder_two]

    spotify_client = MagicMock(spec=SpotifyClient)
    return AlbumProcessor(album_finders, spotify_client)


def test_album_processor_find_albums(album_processor: AlbumProcessor):
    albums = list(album_processor._find_albums())
    expected = [MOCK_ALBUM_ONE, MOCK_ALBUM_TWO]
    assert albums == expected


def test_album_processor_get_songs_from_album(album_processor: AlbumProcessor):
    songs = [
        Song("track one", ["Firstname Lastname", "Someone Else"], "123abc", "111zzz"),
        Song("track two", ["Firstname Lastname"], "123abc", "999aaa"),
    ]
    album_processor._spotify_client.get_songs_from_album.return_value = songs
    assert list(album_processor._get_songs_from_album(MOCK_ALBUM_ONE)) == songs


def test_album_processor_main(album_processor: AlbumProcessor):
    album_processor.main()
