from nhlpy import NHLClient

class StandingsManager:
    
    client = NHLClient(debug=True)

    def get_standings(self):
        standings = self.client.standings.league_standings()
        print(standings)

        # maybe use pandas