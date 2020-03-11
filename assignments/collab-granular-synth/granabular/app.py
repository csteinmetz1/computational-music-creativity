import os
import time
import json
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
from oscapi import osc
from fsapi import fsc


REC = False # whether or not to activate client side grain recording

sliders = [(0, "start", "Control where in the current sound grains are generated from."), 
           (1, "density", "Control how often new grains are triggered."),
           (2, "spray", "Control the level of variation in where grains are generated from."), 
           (3, "pitch", "Transpose the pitch of the sound."), 
           (4, "size", "Control the size of each grain that is generated."), 
           (5, "pan spray", "Control how wide grains are panned across the stereo field.")]
users = []

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

    oscclient = osc()
    fsclient = fsc()

    # top level page
    @app.route("/")
    def root():
        return render_template("index.html")

    # page with project description
    @app.route("/about")
    def about():
        send_grain_file("test123")
        return render_template("about.html")

    @app.route("/join", methods = ["GET", "POST"])
    def join():
        if request.method == "GET":
            if len(users) < len(sliders):
                num_users = len(users) 
                users.append(sliders[num_users])
                return render_template("controller.html", slider=sliders[num_users], rec=REC)
            else:
                return render_template("occupied.html")

        # receive changes for the slider and send via OSC
        if request.method == "POST":
            data = request.get_json()
            if 'slider_id' in data:
                oscclient.send_slider_value(data['slider_id'], data['slider_val'])
            elif 'keyword' in data:
                wavfilepaths = fsclient.download_grains(data['keyword'], n=np.random.randint(1, high=3))
                for wavfilepath in wavfilepaths:
                    grain = os.path.basename(wavfilepath).replace(".wav", "")
                    oscclient.send_grain_file(grain)
            else:
                pass

            return "ok"

    @app.route("/admin", methods = ["GET", "POST"])
    def admin():
        global users
        global sliders

        if request.method == "GET":
            return render_template("admin.html", users=users, len=len(users))

        if request.method == "POST":
            data = request.form
            sliders_to_clear = [int(s) for s in data['clear'].split(',')]
            #for s in sliders_to_clear[::-1]:
            #    del users[s]
            users = []
            return render_template("admin.html", users=users, len=len(users))

    @app.route("/upload", methods = ["POST"])
    def upload():

        # extract the audio data blob
        audio_data = request.files["audioData"]

        # create datacode for new filename
        datecode = datetime.datetime.now().strftime("%H%M%S")
        webmfilepath = f"grains/mic{datecode}.webm"
        wavfilepath  = f"grains/mic{datecode}.wav"

        # write file to disk
        with open(webmfilepath, "wb") as f:
            f.write(audio_data.read())
        
        # convert webm to wav file with ffmpeg
        subprocess.run(["ffmpeg",  "-i",  webmfilepath, \
        "-ac", "1", "-f", "wav", wavfilepath, "-r", "44100", "-loglevel", "quiet"])

        # remove the webm file
        os.remove(webmfilepath)

        # check if the file is silent otherwise normalize
        x, sr = soundfile.read(wavfilepath)
        energy = np.sum(np.power(np.abs(x), 2))/x.shape[0]
        print(f"grain energy: {energy:0.2e}")
        if energy >= 1e-4:
            # normalize and save to disk
            x /= np.max(np.abs(x))
            soundfile.write(wavfilepath, x, sr)
            # send filepath to the new grain via OSC
            oscclient.send_grain_file("mic"+datecode)
        else:
            os.remove(wavfilepath)

        return "ok"

    return app