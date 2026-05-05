import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import requests
import re
import sqlite3

def get_prediction_data(player_stats):
    pred_data = []
    for player in player_stats:
        data = {key:player[key] for key in player.keys() if key not in year_list}
        data = {**data, **get_year_data(player, '20222023', '1'), **get_year_data(player, '20232024', '2')}
        data['season_1'] = '20222023'
        data['season_2'] = '20232024'
        data['season_3'] = '20242025'
        pred_data.append(data)

def fill_dataframe():
    teams = get_all_teams("2023-11-10") # just use current-ish date to get team codes

    players = []
    for team in teams:
        players.append(get_eligible_players_for_all_teams(team, 20222023))

    player_stats = []
    for player in players:
        player_stats.append(get_player_stats(player))

    df = pd.DataFrame(player_stats)
    print(df)

year_list = ['2010-11-10','2011-11-10', '2012-11-10','2013-11-10', '2014-11-10', '2015-11-10', '2016-11-10', '2017-11-10', '2018-11-10', '2019-11-10', '2020-11-10', '2021-11-10', '2022-11-10', '2023-11-10']
season_list = ['20102011', '20112012', '20122013', '20132014', '20142015', '20152016', '20162017', '20172018', '20182019', '20192020', '20202021', '20212022', '20222023', '20232024', '20242025']

def get_all_teams():
    team_abbrevs = []        
    for year in year_list:
        res = requests.get("https://api-web.nhle.com/v1/standings/{}".format(year))
        standings = res.json()

        for team in standings["standings"]:
            team_abbrevs.append(team["teamAbbrev"]["default"])

    team_ids = set(team_abbrevs)

    return team_ids

def get_eligible_players_for_all_teams(all_team_codes):
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

    player_ids = set(players)
    return player_ids # save in database

def get_sqlite_conn():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "instance", "flaskr.sqlite")

    print("DB PATH:", db_path)  # debug

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def save_player_ids(player_ids):
    conn = get_sqlite_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS player_ids (
            player_id TEXT PRIMARY KEY
        )
    """)

    for pid in player_ids:
        cur.execute("""
            INSERT OR IGNORE INTO player_ids (player_id)
            VALUES (?)
        """, (pid,))

    conn.commit()
    conn.close()

def clear_players_table():
    conn = get_sqlite_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM players")

    conn.commit()
    conn.close()

def save_player(conn, data):
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO players (
            player_id, name, country, height, weight, birth_date, position
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["id"],
        data["name"],
        data["country"],
        data["height"],
        data["weight"],
        data["birth_date"],
        data["position"]
    ))

def save_player_season(conn, player_id, season, stats):
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO player_seasons (
            player_id, season,
            goals, assists, shots,
            plus_minus, games_played, avg_toi, team
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        player_id,
        season,
        stats["goals"],
        stats["assists"],
        stats["shots"],
        stats["plus_minus"],
        stats["games_played"],
        stats["avg_toi"],
        stats["team"]
    ))

def get_player_ids():
    conn = get_sqlite_conn()
    cur = conn.cursor()
    cur.execute("SELECT player_id FROM player_ids")
    rows = cur.fetchall()
    return [row[0] for row in rows]

def fetch_and_store_players(ids):
    conn = get_sqlite_conn()

    for player_id in ids:
        res = requests.get(f"https://api-web.nhle.com/v1/player/{player_id}/landing")
        player = res.json()

        if player["position"] == "G":
            continue

        base_data = {
            "name": f"{player['firstName']['default']} {player['lastName']['default']}",
            "country": player["birthCountry"],
            "id": player["playerId"],
            "height": player["heightInInches"],
            "weight": player["weightInPounds"],
            "birth_date": player["birthDate"],
            "position": player["position"],
        }

        # save player
        save_player(conn, base_data)

        # save seasons
        for year_stats in player["seasonTotals"]:
            if (
                str(year_stats["season"]) in season_list and
                year_stats["gameTypeId"] == 2 and
                year_stats["leagueAbbrev"] == "NHL"
            ):
                save_player_season(
                    conn,
                    base_data["id"],
                    str(year_stats["season"]),
                    {
                        "goals": year_stats["goals"],
                        "assists": year_stats["assists"],
                        "shots": year_stats["shots"],
                        "avg_toi": year_stats["avgToi"],
                        "plus_minus": year_stats["plusMinus"],
                        "games_played": year_stats["gamesPlayed"],
                        "team": year_stats["teamName"]["default"],
                    }
                )

    conn.commit()
    conn.close()

def get_eligible_players():
    conn = get_sqlite_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT player_id
        FROM player_seasons
        GROUP BY player_id
        HAVING COUNT(*) >= 3
           AND SUM(games_played) > 100
    """)

    return [row[0] for row in cur.fetchall()]

def get_prediction_dataframe(conn, player_ids):
    rows = []

    for player_id in player_ids:

        query = """
        SELECT
            p.player_id,
            p.name,
            p.height,
            p.weight,
            p.birth_date,
            p.position,

            s.season,
            s.goals,
            s.assists,
            s.shots,
            s.avg_toi,
            s.plus_minus,
            s.games_played

        FROM players p
        JOIN player_seasons s ON p.player_id = s.player_id
        WHERE p.player_id = ?
        ORDER BY s.season DESC
        """

        df = pd.read_sql_query(query, conn, params=[player_id])

        # must have at least 3 seasons
        if len(df) < 3:
            continue

        s1, s2, s3 = df.iloc[0], df.iloc[1], df.iloc[2]

        rows.append({
            "player_id": player_id,
            "name": s1["name"],
            "height": s1["height"],
            "weight": s1["weight"],
            "birth_date": s1["birth_date"],
            "position": s1["position"],

            "goals_1": s1["goals"],
            "assists_1": s1["assists"],
            "shots_1": s1["shots"],
            "avg_toi_1": s1["avg_toi"],
            "plus_minus_1": s1["plus_minus"],
            "games_played_1": s1["games_played"],

            "goals_2": s2["goals"],
            "assists_2": s2["assists"],
            "shots_2": s2["shots"],
            "avg_toi_2": s2["avg_toi"],
            "plus_minus_2": s2["plus_minus"],
            "games_played_2": s2["games_played"],

            "season_3": s3["season"]
        })

    return pd.DataFrame(rows)

# must have 50 games played in each season from 2021-2023
def filter_players(players):

    valid_players = []

    for player in players:
        res = requests.get("https://api-web.nhle.com/v1/player/{}/landing".format(player))
        player_data = res.json()

        valid_seasons = []
        valid = True
        for season in player_data["seasonTotals"]:
            if season["leagueAbbrev"] == "NHL" and season["gameTypeId"] == 2 and (season["season"] == 20212022 or season["season"] == 20222023 or season["season"] == 20232024 or season["season"] == 20242025): 
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
        if (season_stats["season"] == 20212022 or season_stats["season"] == 20222023 or season_stats["season"] == 20232024 or season_stats["season"] == 20242025) and season_stats["gameTypeId"] == 2 and season_stats["leagueAbbrev"] == "NHL":
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
    if time == '0':
        return '0'
    time = time.split(":")
    time = float(time[0] + str((int(time[1])/60))[1:])
    time = round(time, 2)
    return time

def get_age_from_date():
    date = "1986-12-29"

# once ready take in df
def process_data(df):
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
    df["age"] = df["season_3"].astype(str).apply(lambda s: int(s[:4])) - df["birth_date"].apply(lambda s: int(s.split("-")[0]))

    return df

# get player stats version 2
def get_player_stats_v2(ids):
    player_stats = []
    for player in ids:
        res = requests.get("https://api-web.nhle.com/v1/player/{}/landing".format(player))
        player = res.json()
        if player["position"] != "G":
            # only get non-goalies
            data = { 
                "name" : f"{player["firstName"]["default"]} {player["lastName"]["default"]}",
                "country" : player["birthCountry"],
                "id" : player["playerId"] ,
                "height" : player["heightInInches"],
                "weight" : player["weightInPounds"],
                "birth_date" : player["birthDate"],
                "position" : player["position"],
            }
            # get season stats now
            for year_stats in player["seasonTotals"]:
                if str(year_stats["season"]) in season_list and year_stats["gameTypeId"] == 2 and year_stats["leagueAbbrev"] == "NHL":
                    data[str(year_stats["season"])] = {
                        "goals" : year_stats["goals"],
                        "assists" : year_stats["assists"],
                        "shots" : year_stats["shots"],
                        "avg_toi" : year_stats["avgToi"],
                        "plus_minus" : year_stats["plusMinus"],
                        "games_played" : year_stats["gamesPlayed"],
                        "team" : year_stats["teamName"]["default"],
                    }

            player_stats.append(data)
    return player_stats

# atleast 3 seasons and 100 total games
def reduce_player_list(player_stats):
    reduced_player_stats = []
    for player in player_stats:
        games_played = 0
        seasons = 0
        for year in season_list:
            if year in player.keys():
                games_played+=player[year]["games_played"]
                seasons+=1
        if seasons >= 3 and games_played > 100:
            reduced_player_stats.append(player)
    return reduced_player_stats

def get_year_data(player, year, index):
    if year in player.keys():
        return {key+'_'+index:val for key,val in player[year].items()}
    else:
        return {
            "goals_"+index: 0,
            "assists_"+index: 0,
            "shots_"+index: 0,
            "avg_toi_"+index: 0,
            "plus_minus_"+index: 0,
            "games_played_"+index: 0,
        }

split_data = []
def split_seasons(reduced_player_stats):
    print("In split")
    for player in reduced_player_stats:
        for i in range(12):
            years = season_list[i:i+3]
            if years[2] in player.keys():
                data = {key:player[key] for key in player.keys() if key not in season_list}
                data = {**data, **get_year_data(player, years[0], "1"), **get_year_data(player, years[1], "2")}
                data["season_1"] = str(years[0])
                data["season_2"] = str(years[1])
                data["season_3"] = str(years[2])
                data["ppg_3"] = (player[years[2]]["goals"] + player[years[2]]["assists"]) / player[years[2]]["games_played"]
                split_data.append(data)
    

def make_player_stats_final():
    split_seasons()
    df = pd.DataFrame(split_data)
    # print(df)
    df.to_csv('player.csv', index=False)

    df = process_data("player.csv")

    df_final = df[["games_played_1", "games_played_2", "goals_1", "goals_2",
                   "height", "plus_minus_1", "plus_minus_2", "position", "ppg_3",
                   "shots_1", "shots_2", "avg_toi_1", "avg_toi_2",
                   "weight", "points_1", "points_2", "age"]]
    
    df_final = pd.get_dummies(df_final, columns=['position'])
    df_final = df_final[(df_final['games_played_1']!=0)|(df_final['games_played_2']!=0)]
    df_final = df_final.fillna(0)

    print(df_final)
    df_final.to_csv('player_final.csv', index=False)

