import random
from flaskr.db import get_db

class Team:
    def __init__(self, name, elo):
        self.name = name
        self.elo = elo  

class EloManager:

    def win_probability(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400)) # ** is: 2^3 --> 2 ** 3
    
    def update_ratings(self, r_a, r_b, result, k=20):
        p_a = self.win_probability(r_a, r_b)

        r_a_new = r_a + k * (result - p_a)
        r_b_new = r_b + k * ((1 - result) - (1 - p_a))
        return r_a_new, r_b_new
    
    def write_new_elo_db(self, team_name, new_elo):
        db = get_db()
        db.execute(
            "UPDATE elo SET elo = ? WHERE team_name = ?",
            (new_elo, team_name)
        )
        db.commit()
    
    # function only for testing purposes
    def simulate_games(self, team_a_name="Oilers", team_b_name="Canucks", num_games=5):
        
        db = get_db()

        t_a_row = db.execute(
            "SELECT elo FROM elo WHERE team_name = ?", (team_a_name,)
        ).fetchone()

        t_b_row = db.execute(
            "SELECT elo FROM elo WHERE team_name = ?", (team_b_name,)
        ).fetchone()

        t_a = Team(team_a_name, t_a_row["elo"] if t_a_row else 1500)
        t_b = Team(team_b_name, t_b_row["elo"] if t_b_row else 1500)

        result = 1

        for i in range(5):
            team_a_prob = self.win_probability(t_a.elo, t_b.elo)

            num = random.random()
            if num <= team_a_prob:
                result = 1
            else:
                result = 0

            t_a.elo, t_b.elo = self.update_ratings(t_a.elo, t_b.elo, result)

        # update new elos in database
        self.write_new_elo_db(team_a_name, t_a.elo)
        self.write_new_elo_db(team_b_name, t_b.elo)

        print(f"{team_a_name}: {t_a.elo}, {team_b_name}: {t_b.elo}") 

    