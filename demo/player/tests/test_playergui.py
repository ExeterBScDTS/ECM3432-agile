import pytest
import playergui


@pytest.fixture
def gui():
    return playergui.PlayerGUI()


def test_PlayerGUI(gui):
    assert isinstance(gui, playergui.PlayerGUI)
