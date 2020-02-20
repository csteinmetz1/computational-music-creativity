import os
import time
import base64
import random
import datetime
import soundfile
import subprocess
import numpy as np

from flask import Flask, url_for, request
from flask import render_template
import werkzeug

from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
from osc import send_slider_value, send_grain_file

sliders = [(0, "start"), (1, "density"), (2, "spray"), (3, "pitch"), (4, "grain"), (5, "size"), (6, "pan spray")]

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

    # setup OSC comms to localhost
    osc_startup()
    osc_udp_client("127.0.0.1", 4242, "Pd")

    # a simple page that says hello
    @app.route("/",  methods = ["GET", "POST"])
    def root():
        # serve the page
        if request.method == "GET":
            slider = random.choice(sliders)
            return render_template("index.html", slider=slider)

        # receive changes for the slider and send via OSC
        if request.method == "POST":
            data = request.form
            send_slider_value(data['slider_id'], data['slider_val'])
            return "ok"

    @app.route("/upload", methods = ["POST"])
    def upload():

        # extract the audio data blob
        audio_data = request.files["audioData"]

        # create datacode for new filename
        datecode = datetime.datetime.now().strftime("%H%M%S")
        webmfilepath = f"grains/{datecode}.webm"
        wavfilepath  = f"grains/{datecode}.wav"

        # write file to disk
        with open(webmfilepath, "wb") as f:
            f.write(audio_data.read())
        
        # convert webm to wav file with ffmpeg
        subprocess.run(["ffmpeg",  "-i",  webmfilepath, \
        "-ac", "1", "-f", "wav", wavfilepath,  "-loglevel", "quiet"])

        # remove the webm file
        os.remove(webmfilepath)

        # check if the file is silent otherwise normalize
        x, sr = soundfile.read(wavfilepath)
        energy = np.sum(np.power(np.abs(x), 2))/x.shape[0]
        print(f"grain energy: {energy:0.2e}")
        if energy >= 1e-3:
            # normalize and save to disk
            x /= np.max(np.abs(x))
            soundfile.write(wavfilepath, x, sr)
            # send filepath to the new grain via OSC
            send_grain_file(datecode)
        else:
            os.remove(wavfilepath)

        return "ok"

    return app