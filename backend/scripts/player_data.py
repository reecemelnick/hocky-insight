import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flaskr import create_app
import pandas as pd
import requests

from nhlpy.api.query.builder import QueryBuilder, QueryContext
from nhlpy.nhl_client import NHLClient
from nhlpy.api.query.filters.draft import DraftQuery
from nhlpy.api.query.filters.season import SeasonQuery
from nhlpy.api.query.filters.game_type import GameTypeQuery
from nhlpy.api.query.filters.position import PositionQuery, PositionTypes

app = create_app()

with app.app_context():

    def get_all_players():
        players = []
        # players.append(get_player_stats())

    def get_player_stats(id):

        seasons = []

        player_obj = {}
        res = requests.get("https://api-web.nhle.com/v1/player/{}/landing".format(id))
        player = res.json()

        for season_stats in player["seasonTotals"]:
            if season_stats["season"] == 20212022 and season_stats["gameTypeId"] == 2:
                print("adding target year")
                seasons.append(season_stats)
        
        player_obj["name"] = f"{player["firstName"]["default"]} {player["lastName"]["default"]}"
        player_obj["country"] = player["birthCountry"]
        player_obj["id"] = player["playerId"] 
        player_obj["height"] = player["heightInInches"]
        player_obj["weight"] = player["weightInPounds"]

        # first season
        player_obj["goals_1"] = seasons[0]["goals"]
        player_obj["assists_1"] = seasons[0]["assists"]
        player_obj["shots_1"] = seasons[0]["shots"]
        player_obj["avg_toi_1"] = seasons[0]["avgToi"]
        player_obj["plus_minus_1"] = seasons[0]["plusMinus"]
        player_obj["team_1"] = seasons[0]["teamName"]["default"]

        # second season
         
        # ppg third season
        
        # df = pd.DataFrame(player_obj)
        # print(df)
        print(player_obj)
        return player_obj
    
    
    get_player_stats(8478402)