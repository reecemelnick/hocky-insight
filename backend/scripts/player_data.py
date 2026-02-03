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

    def fill_dataframe():
        teams = get_all_teams("2023-11-10")

        players = []
        for team in teams:
            players.append(get_eligible_players_for_team(team, 20222023))

        player_stats = []
        for player in players:
            player_stats.append(get_player_stats(player))

        df = pd.DataFrame(player_stats)
        print(df)

    def get_all_teams(date):
        team_abbrevs = []
        
        res = requests.get("https://api-web.nhle.com/v1/standings/{}".format(date))
        standings = res.json()

        for team in standings["standings"]:
            team_abbrevs.append(team["teamAbbrev"]["default"])

        return team_abbrevs

    # start with players who have 100 games # TODO parse eligible
    def get_eligible_players_for_team(team, year):
        players = []

        res = requests.get("https://api-web.nhle.com/v1/roster/{}/{}".format(team, year))
        team_roster = res.json()

        for forward in team_roster["forwards"]:
            players.append(forward["id"])

        for defensemen in team_roster["defensemen"]:
            players.append(defensemen["id"])

        # call filter_players
        
        return players
    
    # must have 50 games played in each season from 2021-2023
    def filter_players(players):

        valid_players = []
    
        for player in players:
            res = requests.get("https://api-web.nhle.com/v1/player/{}/landing".format(player))
            player_data = res.json()

            valid_seasons = []
            valid = True
            for season in player_data["seasonTotals"]:
                if season["leagueAbbrev"] == "NHL" and season["gameTypeId"] == 2 and (season["season"] == 20212022 or season["season"] == 20222023 or season["season"] == 20232024): 
                    valid_seasons.append(season)
            if len(valid_seasons) < 3:
                print("Not enough seasons")
                continue
            
            for season in valid_seasons:
                if season["gamesPlayed"] < 50:
                    valid = False

            if valid:
                valid_players.append(player)
                print(player_data["lastName"])

        return valid_players

    # currently restricted to seasons 2021-2024 
    def get_player_stats(id):
        seasons = []

        player_obj = {}
        res = requests.get("https://api-web.nhle.com/v1/player/{}/landing".format(id))
        player = res.json()

        for season_stats in player["seasonTotals"]:
            if (season_stats["season"] == 20212022 or season_stats["season"] == 20222023 or season_stats["season"] == 20232024) and season_stats["gameTypeId"] == 2 and season_stats["leagueAbbrev"] == "NHL":
                seasons.append(season_stats)
        
        player_obj["name"] = f"{player["firstName"]["default"]} {player["lastName"]["default"]}"
        player_obj["country"] = player["birthCountry"]
        player_obj["id"] = player["playerId"] 
        player_obj["height"] = player["heightInInches"]
        player_obj["weight"] = player["weightInPounds"]

        print(player["lastName"]["default"])
        print(seasons[1]["season"])
        print(seasons[1]["shots"])

        # first season
        player_obj["goals_1"] = seasons[0]["goals"]
        player_obj["assists_1"] = seasons[0]["assists"]
        player_obj["shots_1"] = seasons[0]["shots"]
        player_obj["avg_toi_1"] = seasons[0]["avgToi"]
        player_obj["plus_minus_1"] = seasons[0]["plusMinus"]
        player_obj["games_played_1"] = seasons[0]["gamesPlayed"]
        player_obj["team_1"] = seasons[0]["teamName"]["default"]

        # second season
        player_obj["goals_2"] = seasons[1]["goals"]
        player_obj["assists_2"] = seasons[1]["assists"]
        player_obj["shots_2"] = seasons[1]["shots"]
        player_obj["avg_toi_2"] = seasons[1]["avgToi"]
        player_obj["plus_minus_2"] = seasons[1]["plusMinus"]
        player_obj["games_played_2"] = seasons[1]["gamesPlayed"]
        player_obj["team_2"] = seasons[1]["teamName"]["default"]
         
        # ppg third season
        player_obj["ppg_3"] = (seasons[2]["points"] / seasons[2]["gamesPlayed"])
        
        return player_obj
    
    # fill_dataframe()

    players = []
    players.append(get_eligible_players_for_team("EDM", 20222023))

    valid_players = filter_players(players[0])
    print(valid_players)

    player_stats = []
    for player in valid_players:
        player_stats.append(get_player_stats(player))


    df = pd.DataFrame(player_stats)
    print(df)

    

