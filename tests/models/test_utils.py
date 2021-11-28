import pytest

from music_scraper.models.utils import normalise_string


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("123abc", "123abc"),
        ("", ""),
        ("   123$%^   ABC ", "123abc"),
    ],
)
def test_normalise_string(input_string: str, expected: str) -> str:
    assert normalise_string(input_string) == expected
