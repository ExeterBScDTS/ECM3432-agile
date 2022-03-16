""" The Playlist class
"""
from dataclasses import dataclass


@dataclass
class Tune:
    name: str
    album: str


@dataclass
class Playlist:
    """Playlist
    Note that tunes is a list, so the usual list methods, append, etc.
    are available.
    """
    tunes: list[Tune]
