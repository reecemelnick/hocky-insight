import random
from .eloManager import Team, EloManager
from flaskr.db import get_db

class SimulationManager:

    def __init__(self):
        self.eloManager = EloManager()

    # function only for testing purposes
    def simulate_games(self, team_a_name="Oilers", team_b_name="Canucks", num_games=5):
        
        db = get_db()

        t_a_row = db.execute(
            "SELECT elo FROM elo WHERE team_name = ?", (team_a_name,)
        ).fetchone()

        t_b_row = db.execute(
            "SELECT elo FROM elo WHERE team_name = ?", (team_b_name,)
        ).fetchone()

        t_a_rating = t_a_row["elo"] if t_a_row else 1500
        t_b_rating = t_b_row["elo"] if t_b_row else 1500
        print(f"{team_a_name}: {t_a_rating}")
        print(f"{team_b_name}: {t_b_rating}")

        t_a = Team(team_a_name, t_a_rating)
        t_b = Team(team_b_name, t_b_rating)

        result = 1

        for i in range(num_games):
            team_a_prob = self.eloManager.win_probability(t_a.elo, t_b.elo)

            num = random.random()
            if num <= team_a_prob:
                result = 1
            else:
                result = 0

            t_a.elo, t_b.elo = self.eloManager.update_ratings(t_a.elo, t_b.elo, result)

        # update new elos in database
        self.eloManager.write_new_elo_db(team_a_name, t_a.elo)
        self.eloManager.write_new_elo_db(team_b_name, t_b.elo)

        print(f"{team_a_name}: {t_a.elo}, {team_b_name}: {t_b.elo}")
