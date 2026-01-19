from flaskr.db import get_db, reset_elo_helper
from datetime import date, timedelta
from flaskr.services.scores import ScoreManager
from flaskr.services.eloRetriever import EloRetriever

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

    # more use for testing and getting back logged games
    def run_though_day(self, date):
        score_manager = ScoreManager() 
        score_data = score_manager.get_scores_specific_date(date)
        if score_data is None:
            return

        for item in score_data:
            self.process_game(item)

    def get_elo_data(self, game):
        eloR = EloRetriever()
        away_team_row = eloR.get_elo_for_team(game["away_name"])
        home_team_row = eloR.get_elo_for_team(game["home_name"])

        away_team_rating = away_team_row["elo"] 
        home_team_rating = home_team_row["elo"]

        return away_team_rating, home_team_rating
    
    def process_game(self, game):

        away_team_rating, home_team_rating = self.get_elo_data(game)

        team_a = Team(game["away_name"], away_team_rating)
        team_b = Team(game["home_name"], home_team_rating)

        if game["away_score"] > game["home_score"]:
            result = 1
        else:
            result = 0

        # return new elo scores based off old ones - depending on outcome of the match
        team_a.elo, team_b.elo = self.update_ratings(team_a.elo, team_b.elo, result)

        # update new elos in database
        self.write_new_elo_db(game["away_name"], team_a.elo)
        self.write_new_elo_db(game["home_name"], team_b.elo)

    def set_elo_from_season_start(self):
        season_start = date(2025, 10, 11)
        end_date = date.today()

        reset_elo_helper() # make sure teams start back at base elo

        curr_date = season_start
        while curr_date <= end_date:
            self.run_though_day(curr_date)
            curr_date += timedelta(days=1)