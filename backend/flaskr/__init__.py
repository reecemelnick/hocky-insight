import os

from flask import Flask
from utils.scores import ScoreManager
from flask_cors import CORS
from flask import request

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
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

    score_manager = ScoreManager()

    # a simple page that give todays scores
    @app.route('/scores')
    def scores():
        date = request.args.get("date", "2026-01-06")
        return score_manager.get_scores_specific_date(date)

    return app
