import os # used for file system paths and folders
from flask import Flask
from flask_cors import CORS
from .routes.scores import bp as scores_bp
from .routes.rankings import bp as rankings_bp
from .db import init_db_command, reset_elo_command, insert_elo_command, clear_last_date_command, close_db
from .services.updateManager import UpdateManager

# flask --app flaskr run --debug --port 8000
def create_app(test_config=None):
    print("App created...")
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app) # tighted later CORS(app, origins=["react origin"])
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # update manager used to check for new day - if new day, process the events
    updateManager = UpdateManager()

    # implemnt when test are added
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
    
    # check for new day # could move to cron job or background worker
    @app.before_request
    def daily_check():
        updateManager.run_daily_tasks_if_needed()

    add_commands(app) # add all click cli commands

    app.teardown_appcontext(close_db)

    app.register_blueprint(scores_bp, url_prefix="/api")
    app.register_blueprint(rankings_bp, url_prefix="/api")

    return app

def add_commands(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(reset_elo_command)
    app.cli.add_command(insert_elo_command)
    app.cli.add_command(clear_last_date_command)

    return
