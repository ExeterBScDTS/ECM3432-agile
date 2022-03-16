import logging
from queue import Queue
from tkinter import Tk, ttk, Button, StringVar, Label, Listbox

logger = logging.getLogger(__name__)


class PlayerGUI:
    """_summary_
    """
    def __init__(self):
        """Constructor for a simple tkinter GUI
        """
        self.__root = Tk()
        self.__root.title(__name__)

        label0 = Label(self.__root, text="    ")
        label0.grid(column=0, row=0)

        label1 = Label(self.__root, text="Albums")
        label1.grid(column=1, row=0)

        label2 = Label(self.__root, text="Tracks")
        label2.grid(column=2, row=0)

        label3 = Label(self.__root, text="Playlist")
        label3.grid(column=3, row=0)

        self.start_button = Button(self.__root, text="Play", command=self.play)
        self.start_button.grid(column=0, row=1)

        self.stop_button = Button(self.__root, text="Pause", command=self.pause)
        self.stop_button.grid(column=0, row=2)

        self.albums_var = StringVar(value=[])
        self.album_list = Listbox(self.__root, height=10, listvariable=self.albums_var)
        self.album_list.grid(column=1, row=1, rowspan=2)
        self.album_list.bind("<<ListboxSelect>>", self.album_sel)

        self.tracks_var = StringVar(value=[])
        self.track_list = Listbox(self.__root, height=10, listvariable=self.tracks_var)
        self.track_list.grid(column=2, row=1, rowspan=2)
        self.track_list.bind("<<ListboxSelect>>", self.track_sel)

        self.playlist = []
        self.playlist_var = StringVar(value=self.playlist)
        self.playlist_list = Listbox(self.__root, height=10, listvariable=self.playlist_var)
        self.playlist_list.grid(column=3, row=1, rowspan=2)
        self.playlist_list.bind("<<ListboxSelect>>", self.playlist_sel)

        self.db_cmd = None
        self.db_data = None
        self._state = "ready"
        self.__next_tune = 0

    def set_albums(self, albums):
        self.albums = albums
        self.albums_var.set(albums)

    def album_sel(self, evt):
        print(evt)
        sel = self.album_list.curselection()[0]
        logger.debug(f"selected {self.albums[sel]}")
        self.db_cmd = "tracks"
        self.db_data = self.albums[sel]

    def set_tracks(self, tracks):
        self.tracks = tracks
        self.tracks_var.set(tracks)

    def track_sel(self, evt):
        print(evt)
        sel = self.track_list.curselection()[0]
        logger.debug(f"Track selected {self.tracks[sel]}")
        self.playlist.append(self.tracks[sel])
        self.playlist_var.set(self.playlist)


    def playlist_sel(self, evt):
        print(evt)
        sel = self.playlist_list.curselection()[0]
        logger.debug(f"Playlist item selected {self.playlist[sel]}")
        self.playlist.pop(sel)
        self.playlist_var.set(self.playlist)
    
    def next_play(self):
        if len(self.playlist) > 0:
            self.__next_tune += 1
            return self.playlist[self.__next_tune - 1]
        else:
            return None

    def play(self):
        """The play action.
        """
        logger.debug("play")
        self._state = "load"

    def pause(self):
        """The pause action.
        """
        logger.debug("pause")
        self._state = "paused"

    def _after(self):
        self.__root.after(self._ms, self._after)
        self._func()

    def set_after(self, ms, func):
        self.__root.after(ms, self._after)
        self._ms = ms
        self._func = func

    def state(self):
        return(self._state)

    def mainloop(self):
        self.__root.mainloop()


if __name__ == "__main__":
    gui = PlayerGUI()
    gui.mainloop()

