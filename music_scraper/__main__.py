from music_scraper.album_processor import AlbumProcessor
from music_scraper.album_finders import (
    AlbumFinderAOTY,
)
from music_scraper.clients import HTTPClient, SpotifyClient
from music_scraper.settings import SpotifyConfig


http_client = HTTPClient()
spotify_client = SpotifyClient(
    http_client,
    SpotifyConfig.CLIENT_ID,
    SpotifyConfig.CLIENT_SECRET,
)

album_finder_aoty = AlbumFinderAOTY(http_client)
album_finders = [album_finder_aoty]

app = AlbumProcessor(album_finders, spotify_client)


if __name__ == "__main__":
    app.main()
