from nhlpy import NHLClient
# from pprint import pprint 

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
