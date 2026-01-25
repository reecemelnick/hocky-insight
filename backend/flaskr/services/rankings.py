from .eloRetriever import EloRetriever

class RankingManager:
    
    eloR = EloRetriever()

    def get_ranked_teams(self):
        rankings_serial = []
        rankings = self.eloR.get_ranked_by_elo()
        for i in rankings:
            rankings_serial.append(
                {
                    "team_name": i["team_name"],
                    "elo": int(i["elo"]),
                }
            )
        return rankings_serial