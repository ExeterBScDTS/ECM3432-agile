import os
import logging
from flask import Flask, Response, jsonify

import player.musicdb as muscicdb
from io import BytesIO

logging.basicConfig(level=logging.DEBUG)

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # apply the blueprints to the app
    from musicplayer import page
    app.register_blueprint(page.bp) 
    app.add_url_rule("/", endpoint="index")

    # album tracklist
    @app.route("/tracks/<path:album>")
    def tracks(album):
        db = muscicdb.MusicDB("file:music.db?mode=ro")
        
        logging.debug(f"fetching tracklist for: {album}")

        tracks = db.get_track_names(album)
        return jsonify(tracks)

    # audio streaming
    @app.route("/music/<string:album>/<path:tune>")
    def streamwav(album,tune):
        """ Stream WAV audio.
        To stream other formats the code required is the same,
        just be sure to set the correct mimetype in Respose.
        e.g. "audio/ogg"
        """
        logging.debug(f"streaming:{album}/{tune}")

        try:
            db = muscicdb.MusicDB("file:music.db?mode=ro")
            stream = db.get_content(tune)
            fwav = BytesIO(stream)
        # get_content throws an exception if the tune can't be found
        # should be fixed, but this way MusicDB can stay as it is.
        except:
            logging.debug(f"no tune: {tune}")
            return ""

        def generate():       
                data = fwav.read(1024)
                while data:
                    yield data
                    data = fwav.read(1024)
        # Assume mimetype for now.  Would be better to have this in the database.
        return Response(generate(), mimetype="audio/x-wav")
   
    return app
