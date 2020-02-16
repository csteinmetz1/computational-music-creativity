import os

from flask import Flask, url_for, request
from flask import render_template

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_url_path="", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello',  methods = ['GET', 'POST'])
    def hello():
        if request.method == 'GET':
            url_for('static', filename='js/tx.js')
            message = "Granabular"
            return render_template('index.html', message=message)
        if request.method == 'POST':
            data = request.form
            print(request.form)
            return "ok"

    return app