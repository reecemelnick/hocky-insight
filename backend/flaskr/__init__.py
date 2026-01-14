import os

from flask import Flask
from flask_cors import CORS
from .routes.scores import bp as scores_bp
from .db import close_db
from .db import init_db_command, seed_db_command, reset_elo_command, insert_elo_command

# flask --app flaskr run --debug --port 8000
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

    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
    app.cli.add_command(reset_elo_command)
    app.cli.add_command(insert_elo_command)

    app.teardown_appcontext(close_db)

    app.register_blueprint(scores_bp)

    return app
