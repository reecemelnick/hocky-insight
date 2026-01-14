import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flaskr import create_app
from flaskr.services.eloManager import EloManager
from flaskr.services.simulations import SimulationManager

app = create_app()

with app.app_context():
    elo = EloManager()
    sim = SimulationManager()
    # sim.simulate_games(num_games=1)
    elo.run_though_day("2025-11-10")