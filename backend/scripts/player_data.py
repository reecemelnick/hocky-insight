import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flaskr import create_app
import pandas as pd
import requests
import re

app = create_app()

with app.app_context():

    def fill_dataframe():
        teams = get_all_teams("2023-11-10") # just use current-ish date to get team codes

        players = []
        for team in teams:
            players.append(get_eligible_players_for_team(team, 20222023))

        player_stats = []
        for player in players:
            player_stats.append(get_player_stats(player))

        df = pd.DataFrame(player_stats)
        print(df)
    
    year_list = ['2010-11-10','2011-11-10', '2012-11-10','2013-11-10', '2014-11-10', '2015-11-10', '2016-11-10', '2017-11-10', '2018-11-10', '2019-11-10', '2020-11-10', '2021-11-10', '2022-11-10', '2023-11-10']
    season_list = ['20102011','20112012', '20122013','20132014', '20142015', '20152016', '20162017', '20172018', '20182019', '20192020', '20202021', '20212022', '20222023','20232024']

    def get_all_teams():
        team_abbrevs = []        
        for year in year_list:
            res = requests.get("https://api-web.nhle.com/v1/standings/{}".format(year))
            standings = res.json()

            for team in standings["standings"]:
                team_abbrevs.append(team["teamAbbrev"]["default"])

        team_ids = set(team_abbrevs)

        return team_ids

    all_team_codes = []
    # all_team_codes = get_all_teams()

    # start with players who have 100 games # TODO parse eligible
    def get_eligible_players_for_team():
        players = []

        for team in all_team_codes:
            for year in season_list:

                res = requests.get("https://api-web.nhle.com/v1/roster/{}/{}".format(team, year))

                try:
                    team_roster = res.json()

                    for forward in team_roster["forwards"]:
                        players.append(forward["id"])

                    for defensemen in team_roster["defensemen"]:
                        players.append(defensemen["id"])
                except:
                    pass

        # valid_players = filter_players(players)

        player_ids = set(players)
        print(player_ids)
        print(len(player_ids))
        
        return player_ids
    
    # player_id = get_eligible_players_for_team()
    
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
                continue
            
            for season in valid_seasons:
                if season["gamesPlayed"] < 50:
                    valid = False

            if valid:
                valid_players.append(player)

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
        player_obj["birth_date"] = player["birthDate"]
        player_obj["position"] = player["position"]

        # first season
        player_obj["goals_1"] = seasons[0]["goals"]
        player_obj["assists_1"] = seasons[0]["assists"]
        player_obj["shots_1"] = seasons[0]["shots"]
        player_obj["avg_toi_1"] = seasons[0]["avgToi"]
        player_obj["plus_minus_1"] = seasons[0]["plusMinus"]
        player_obj["games_played_1"] = seasons[0]["gamesPlayed"]
        player_obj["team_1"] = seasons[0]["teamName"]["default"]
        player_obj["season_1"] = seasons[0]["season"]

        # second season
        player_obj["goals_2"] = seasons[1]["goals"]
        player_obj["assists_2"] = seasons[1]["assists"]
        player_obj["shots_2"] = seasons[1]["shots"]
        player_obj["avg_toi_2"] = seasons[1]["avgToi"]
        player_obj["plus_minus_2"] = seasons[1]["plusMinus"]
        player_obj["games_played_2"] = seasons[1]["gamesPlayed"]
        player_obj["team_2"] = seasons[1]["teamName"]["default"]
        player_obj["season_2"] = seasons[1]["season"]
         
        # ppg third season
        player_obj["season_3"] = seasons[2]["season"]
        player_obj["ppg_3"] = (seasons[2]["points"] / seasons[2]["gamesPlayed"])
        
        return player_obj
    
    def format_ice_time(time):
        time = time.split(":")
        time = float(time[0] + str((int(time[1])/60))[1:])
        time = round(time, 2)
        return time
    
    def get_age_from_date():
        date = "1986-12-29"


    # once ready take in df
    def process_data(file_name):

        df = pd.read_csv(file_name)
        df["points_1"] = (df["goals_1"] + df["assists_1"]) / df["games_played_1"]
        df["points_2"] = (df["goals_2"] + df["assists_2"]) / df["games_played_2"]
        df["goals_1"] = df["goals_1"] / df["games_played_1"]
        df["goals_2"] = df["goals_2"] / df["games_played_2"]
        df["shots_1"] = df["shots_1"] / df["games_played_1"]
        df["shots_2"] = df["shots_2"] / df["games_played_2"]
        df["games_played_1"] = df["games_played_1"] / 82
        df["games_played_2"] = df["games_played_2"] / 82
        df["avg_toi_1"] = df["avg_toi_1"].apply(format_ice_time)
        df["avg_toi_2"] = df["avg_toi_2"].apply(format_ice_time)
        df["age"] = 2024 - df["birth_date"].apply(lambda s: int(s.split("-")[0]))

        return df
    
    with open("player_ids.txt", "r", encoding="utf-8-sig") as f:
        content = f.read()
    ids = re.findall(r"\d+", content)

    # temp
    ids = ['8474157', '8474161', '8474162', '8474163']
    
    # get player stats version 2
    def get_player_stats_v2():
        player_stats = []
        for player in ids:
            res = requests.get("https://api-web.nhle.com/v1/player/{}/landing".format(player))
            player = res.json()
            if player["position"] != "G":
                print(player["lastName"]["default"])
                # only get non-goalies
                data = { 
                    "name" : f"{player["firstName"]["default"]} {player["lastName"]["default"]}",
                    "country" : player["birthCountry"],
                    "id" : player["playerId"] ,
                    "height" : player["heightInInches"],
                    "weight" : player["weightInPounds"],
                    "birthdate" : player["birthDate"],
                    "position" : player["position"],
                }
                # get season stats now

    
    get_player_stats_v2()

    # valid_players = get_eligible_players_for_team("VAN", 20222023)

    # player_stats = []
    # for player in ids:
    #     player_stats.append(get_player_stats(player))

    # df = pd.DataFrame(player_stats)
    # df.to_csv('player.csv', index=False)
    # print(df)

    # df = process_data()
    # df_final = df[["games_played_1", "games_played_2", "goals_1", "goals_2",
    #                "height", "plus_minus_1", "plus_minus_2", "position", "ppg_3",
    #                "shots_1", "shots_2", "avg_toi_1", "avg_toi_2",
    #                "weight", "points_1", "points_2", "age"]]
    
    # # transform position columns into one-hot encoded features
    # df_final = pd.get_dummies(df_final, columns=["position"])
    # df_final.to_csv('oilers_final.csv', index=False)

    # just start with one team to get a benchmark
    

    

 