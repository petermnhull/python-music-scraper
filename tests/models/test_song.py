import pytest

from music_scraper.models import Song, SpotifyAlbumTrack
from music_scraper.models.spotify_album_search import SpotifyArtist


@pytest.mark.parametrize(
    "track, album_id, expected",
    [
        (
            SpotifyAlbumTrack(id="xyz789", name="track name", artists=[SpotifyArtist(name="bob")]),
            "123abc",
            Song(
                title="track name", artists=["bob"], spotify_album_id="123abc", spotify_id="xyz789"
            ),
        ),
    ],
)
def test_song_from_spotify_track(track: SpotifyAlbumTrack, album_id: str, expected: Song):
    assert Song.from_spotify_track(track, album_id) == expected
