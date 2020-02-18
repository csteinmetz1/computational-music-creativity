import os
import base64
import datetime

from flask import Flask, url_for, request
from flask import render_template
import werkzeug

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_url_path="", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # create dir for grain storage
    try:
        os.makedirs("grains")
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/",  methods = ["GET", "POST"])
    def root():
        # serve the page
        if request.method == "GET":
            message = "Granabular"
            return render_template("index.html", message=message)

        # receive changes for the slider
        if request.method == "POST":
            data = request.form
            print(request.form)

            return "ok"

    @app.route("/upload", methods = ["POST"])
    def upload():

        # extract the audio data blob
        audio_data = request.files["audioData"]

        # create datacode for new filename
        datecode = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        # write file to disk
        with open(f"grains/{datecode}.webm", "wb") as f:
            f.write(audio_data.read())

        return "ok"

    return app