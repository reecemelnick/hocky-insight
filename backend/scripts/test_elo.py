import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flaskr import create_app
from flaskr.services.eloManager import EloManager

app = create_app()

with app.app_context():
    elo = EloManager()
    elo.simulate_games()
