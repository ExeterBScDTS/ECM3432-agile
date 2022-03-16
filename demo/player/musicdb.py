import sqlite3
import logging

logger = logging.getLogger(__name__)


class MusicDB:
    """
    Interface to a SQLite3 database.
    Note that sqlite3 is thread safe, for reading, but requires
    check_same_thread=False is set in calls to connect().  By
    default check_same_thread is True, so we leave it this way
    and only access the DB from one thread.
    """
    def __init__(self, connection_uri: str) -> None:
        """
        :param connection_uri: a valid URI, e.g. "file:music.db?mode=rw"
        :type connection_uri: str
        """
        self.__connection_uri = connection_uri
        self.verify_connection()
        pass

    def verify_connection(self):
        """Ensure connection to the database is possible.
        """
        con = sqlite3.connect(self.__connection_uri, uri=True)
        con.close()
        pass

    def get_album_names(self) -> tuple:
        logger.debug("get_album_names")
        with sqlite3.connect(self.__connection_uri, uri=True) as con:
            cur = con.cursor()
            cur.execute('SELECT DISTINCT album FROM tunes')
            albums = []
            for i in cur:
                albums.append(i[0])
        return tuple(albums)

    def get_track_names(self, album_name: str) -> tuple:
        logger.debug("get_track_names")
        with sqlite3.connect(self.__connection_uri, uri=True) as con:
            cur = con.cursor()
            cur.execute('SELECT name FROM tunes WHERE album=?', (album_name,))
            tracks = []
            for i in cur:
                tracks.append(i[0])
        return tuple(tracks)

    def get_content(self, track_name: str) -> bytes:
        with sqlite3.connect(self.__connection_uri, uri=True) as con:
            cur = con.cursor()
            cur.execute('SELECT content FROM tunes WHERE name=?', (track_name,))
            row = cur.fetchone()
            return row[0]
