import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flaskr import create_app
from flaskr.services.eloManager import EloManager
from flaskr.services.simulations import SimulationManager
from flaskr.services.scores import ScoreManager
from flaskr.services.updateManager import UpdateManager
from flaskr.services.rankings import RankingManager
from flaskr.services.nhlStandings import StandingsManager
from nhlpy import NHLClient
import pandas as pd
import requests


app = create_app()

with app.app_context():
    elo = EloManager()
    sim = SimulationManager()
    score = ScoreManager()
    up = UpdateManager()
    rank = RankingManager()
    standings = StandingsManager()
    standings.get_standings()

    
    # client = NHLClient(debug=True)
    # scores = client.game_center.daily_scores()

    # games = pd.json_normalize(scores["games"])
    # print(games.head())
    # print(games.keys())

    # df = pd.DataFrame(scores)
