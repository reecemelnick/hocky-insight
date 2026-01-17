import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flaskr import create_app
from flaskr.services.eloManager import EloManager
from flaskr.services.simulations import SimulationManager
from flaskr.services.scores import ScoreManager
from flaskr.services.updateManager import UpdateManager

app = create_app()

with app.app_context():
    elo = EloManager()
    sim = SimulationManager()
    score = ScoreManager()
    up = UpdateManager()
    up.get_last_date()
    # sim.simulate_games(num_games=1)
    # elo.run_though_day("2025-11-10")
    # print(elo.check_new_day("2026-01-15"))
    # print(score.get_scores_specific_date("2026-01-16"))