from nhlpy import NHLClient
from pprint import pprint

class ScoreManager:

    # api access
    client = NHLClient(debug=True)

    def get_todays_scores(self):
        # get todays scores only
        scores = self.client.game_center.daily_scores()
        return scores

    def get_scores_specific_date(self, new_date):

        print(new_date) # TODO add checking and ignore days that have no games

        # get scores from specific date
        try:
            scores_dict = self.client.game_center.daily_scores(date=new_date)
            games = scores_dict.get("games", [])
            # print(f"games: {games}")
            if not games:
                return []
        except Exception as e:
            return []

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
