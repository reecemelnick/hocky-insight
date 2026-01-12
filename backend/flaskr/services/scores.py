from nhlpy import NHLClient
from datetime import datetime, timedelta

class ScoreManager:

    # api access
    client = NHLClient(debug=True)

    def get_todays_scores(self):
        # get todays scores only
        scores = self.client.game_center.daily_scores()
        return scores
    
    def parse_scores(self, games):
        game_scores = []
        for game in games:
            away_team = game["awayTeam"]
            home_team = game["homeTeam"]
            away_logo = away_team["logo"]
            home_logo = home_team["logo"]
            winner = self.get_winner(home_team, away_team)
            print(f"Winner: {winner}")

            game_scores.append(
                    {
                        "away_name": away_team["name"]['default'],
                        "away_score": away_team["score"], 
                        "home_name": home_team["name"]['default'],
                        "home_score": home_team["score"],
                        "away_logo": away_logo,
                        "home_logo": home_logo,
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
    
    # FIX THIS
    
s = ScoreManager()
# print(s.get_last_ten("Oilers"))