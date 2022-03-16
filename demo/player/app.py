""" A prototype music player
"""
import logging
from playergui import PlayerGUI
from musicdb import MusicDB
from wavplay import WavPlay
from threading import Thread
from queue import Empty, Queue
from time import sleep



logger = logging.getLogger(__name__)


class PlayerThread(Thread):
    """
    """
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, daemon=True):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.args = args
        self.kwargs = kwargs
        self.player = WavPlay()
        self.player.paused = True

    def run(self):
        """
        """
        queueIn: Queue = self.args[0]
        #  queueOut: Queue = self.args[1]
        while True:
            try:
                msg = queueIn.get_nowait()
                queueIn.task_done()
                if msg["cmd"] == "pause":
                    self.player.paused = True
                elif msg["cmd"] == "play":
                    self.player.paused = False
                elif msg["cmd"] == "load":
                    self.player.load(msg["data"])
            except Empty:
                pass
            if self.player.paused:
                #  queueOut.put("paused")
                sleep(0.1)
            else:
                self.player.play()
                #  queueOut.put("playing")


class DatabaseThread(Thread):
    """
    """
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, daemon=True):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.args = args
        self.kwargs = kwargs
        # Open DB in read-only mode
        self.db = MusicDB("file:music.db?mode=ro")

    def run(self):
        """
        """
        queueIn: Queue = self.args[0]
        queueOut: Queue = self.args[1]
        while True:
            msg = queueIn.get()
            queueIn.task_done()
            if msg["cmd"] == "albums":
                albums = self.db.get_album_names()
                queueOut.put({"from": "db", "cmd": "albums", "data": albums})
            elif msg["cmd"] == "tracks":
                tracks = self.db.get_track_names(msg["data"])
                queueOut.put({"from": "db", "cmd": "tracks", "data": tracks})
            elif msg["cmd"] == "content":
                content = self.db.get_content(msg["data"])
                queueOut.put({"from": "db", "cmd": "content", "data": content})


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("Starting")
    # Create the GUI, but don't run mainloop() yet
    gui = PlayerGUI()
    feedbackQueue = Queue()
    gui.feedback = feedbackQueue
    playQueue = Queue()
    player = PlayerThread(args=(playQueue, feedbackQueue))
    player.start()
    dbQueue = Queue()
    db = DatabaseThread(args=(dbQueue, feedbackQueue))
    db.start()

    # Note that we can access methods and properties of the gui
    # because this main thread is the gui thread.  We should not
    # directly access objects in other threads.

    def body():
        if gui._state == "load":
            gui._state = "play"
            next_tune = gui.next_play()
            if next_tune:
                dbQueue.put({"cmd": "content", "data": next_tune})
        elif gui._state == "paused":
            playQueue.put({"cmd": "pause"})
        else:
            playQueue.put({"cmd": "play"})

        if gui.db_cmd:
            dbQueue.put({"cmd": gui.db_cmd, "data": gui.db_data})
            gui.db_cmd = None
        try:
            msg = feedbackQueue.get_nowait()
            feedbackQueue.task_done()
            logger.debug(f"feedback: {msg['from']}/{msg['cmd']}")
            if msg["from"] == "db":
                if msg["cmd"] == "albums":
                    gui.set_albums(msg["data"])
                elif msg["cmd"] == "tracks":
                    logger.debug(f"SETTING: {msg}")
                    gui.set_tracks(msg["data"])
                elif msg["cmd"] == "content":
                    playQueue.put({"cmd": "load", "data": msg["data"]})

        except Empty:
            pass

    # If no database available can insert data to play like this -
    # with open("sample.wav", "rb") as f:
    #    playQueue.put({"cmd": "load", "data": f.read()})

    dbQueue.put({"cmd": "albums"})
    gui.set_after(200, body)
    gui.mainloop()
