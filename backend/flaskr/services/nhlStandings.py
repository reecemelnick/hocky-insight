from nhlpy import NHLClient

class StandingsManager:
    
    client = NHLClient(debug=True)

    def get_standings(self):
        standings = self.client.standings.league_standings()
        teams = standings["standings"]

        standings = []

        for team in teams:
            standings.append(
                {
                    "team_name": team["teamCommonName"]["default"],
                    "wins": team["regulationPlusOtWins"],
                    "loss": team["losses"],
                    "otLoss": team["otLosses"],
                    "points": team["points"]
                }
            )

        return standings