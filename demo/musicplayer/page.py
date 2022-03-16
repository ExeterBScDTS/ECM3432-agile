from flask import Blueprint
from flask import render_template
from flask import request
import logging

import player.musicdb as muscicdb

bp = Blueprint("page", __name__)

@bp.route("/")
def index():

    albumData = []

    db = muscicdb.MusicDB("file:music.db?mode=ro")
    albums = db.get_album_names()

    # Want list in a different format as planning to have
    # album ref/id not always be displayed name.
    for album in albums:
        albumData.append({"id": album, "title": album[0:-1]})

    return render_template("page/index.html", albums=albumData)
