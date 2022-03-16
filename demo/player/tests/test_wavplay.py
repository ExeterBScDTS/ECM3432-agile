import pytest
import wavplay


@pytest.fixture
def player():
    return wavplay.WavPlay()


def test_WavPlay(player):
    assert isinstance(player, wavplay.WavPlay)
