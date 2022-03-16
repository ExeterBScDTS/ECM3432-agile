import pytest
import musicdb


@pytest.fixture
def db():
    return musicdb.MusicDB("file://BAD")


def test_MusicDB(db):
    assert isinstance(db, musicdb.MusicDB)