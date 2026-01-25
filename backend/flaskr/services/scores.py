from nhlpy import NHLClient
from datetime import datetime, timedelta
from .eloRetriever import EloRetriever

class ScoreManager:

    # api access
    client = NHLClient(debug=True)

    def get_todays_scores(self):
        # get todays scores only
        scores = self.client.game_center.daily_scores()
        return scores
    
    def parse_scores(self, games):
        eloR = EloRetriever()
        
        game_scores = []
        for game in games:
            away_team = game["awayTeam"]
            home_team = game["homeTeam"]
            away_logo = away_team["logo"]
            home_logo = home_team["logo"]

            if "score" not in away_team or "score" not in home_team:
                away_team_score = ""
                home_team_score = ""
                winner = ""
            else:
                away_team_score = away_team["score"]
                home_team_score = home_team["score"]
                winner = self.get_winner(away_team, home_team)

            away_elo = int(eloR.get_elo_for_team(away_team["name"]['default'])["elo"])
            home_elo = int(eloR.get_elo_for_team(home_team["name"]['default'])["elo"])

            

            game_scores.append(
                    {
                        "away_name": away_team["name"]['default'],
                        "away_score": away_team_score, 
                        "home_name": home_team["name"]['default'],
                        "home_score": home_team_score,
                        "away_logo": away_logo,
                        "home_logo": home_logo,
                        "away_elo": away_elo,
                        "home_elo": home_elo,
                        "winner": winner,
                    }
                )
            
        return game_scores
    
    def get_winner(self, away_team, home_team):
        if home_team["score"] > away_team["score"]:
            return home_team["name"]['default']
        else:
            return away_team["name"]['default']

    def get_scores_specific_date(self, new_date):

        # get scores from specific date
        try:
            scores_dict = self.client.game_center.daily_scores(date=new_date)
        except Exception as e:
            raise

        games = scores_dict.get("games", [])
        if not games:
            print("No games in list")
            return None

        return self.parse_scores(games)
    

