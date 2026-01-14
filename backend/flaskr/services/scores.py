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

            print("AWAY:", eloR.get_elo_for_team(away_team["name"]["default"])["elo"])
            print("HOME:", eloR.get_elo_for_team(home_team["name"]["default"])["elo"])

            game_scores.append(
                    {
                        "away_name": away_team["name"]['default'],
                        "away_score": away_team["score"], 
                        "home_name": home_team["name"]['default'],
                        "home_score": home_team["score"],
                        "away_logo": away_logo,
                        "home_logo": home_logo,
                        "away_elo": eloR.get_elo_for_team(away_team["name"]['default'])["elo"],
                        "home_elo": eloR.get_elo_for_team(home_team["name"]['default'])["elo"],
                    }
                )
        return game_scores
    
    def get_winner(self, home_team, away_team):
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
    
    # FIX THIS
    def get_last_ten(self, team):
        
        results = []

        today = datetime.today()
        start_date = today - timedelta(days=3)
        end_date = today - timedelta(days=1)

        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
    
            try:
                scores_dict = self.client.game_center.daily_scores(date=date_str)
            except Exception as e:
                current_date += timedelta(days=1)
                continue

            games = scores_dict.get("games" , [])
            for game in games:
                if game["homeTeam"]["name"]['default'] == team or game["awayTeam"]["name"]['default'] == team:
                    results.append(game)
                
            current_date += timedelta(days=1)

        return results

    
s = ScoreManager()
# print(s.get_last_ten("Oilers"))