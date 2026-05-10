import pandas as pd
import sqlite3
import requests
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class PlayerFill:

  def add_players_by_year(self, year):
    team_ids = self.get_all_teams_for_year(year)
    print(team_ids)
    self.get_player_ids(team_ids, year)
  

  def get_all_teams_for_year(self, year):
    team_abbrevs = []        

    print(self.change_season_format(year))
  
    res = requests.get("https://api-web.nhle.com/v1/standings/{}".format(self.change_season_format(year)))
    standings = res.json()

    for team in standings["standings"]:
        team_abbrevs.append(team["teamAbbrev"]["default"])

    team_ids = set(team_abbrevs)

    return team_ids
  
  def change_season_format(self, season):
     new_format = ""
     new_format += (season[:4] + "-11-10")
     return new_format

  def get_player_ids(self, all_team_codes, year):
    conn = self.get_sqlite_conn()

    for team in all_team_codes:
      res = requests.get("https://api-web.nhle.com/v1/roster/{}/{}".format(team, year))
      
      team_roster = res.json()

      for forward in team_roster["forwards"]:
          print(forward["id"])
          self.add_player(conn, forward["id"])

      for defensemen in team_roster["defensemen"]:
          print(defensemen["id"])
          self.add_player(conn, defensemen["id"])
      
    conn.commit()
    conn.close()
  
  def get_sqlite_conn(self):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "instance", "flaskr.sqlite")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
  
  def add_player(self, conn, id):
     
    res = requests.get(f"https://api-web.nhle.com/v1/player/{id}/landing")
    player = res.json()

    base_data = {
        "name": f"{player['firstName']['default']} {player['lastName']['default']}",
        "country": player["birthCountry"],
        "id": player["playerId"],
        "height": player["heightInInches"],
        "weight": player["weightInPounds"],
        "birth_date": player["birthDate"],
        "position": player["position"],
    }

    self.save_player(conn, base_data)
    self.add_all_seasons_for_player(conn, player, base_data)

  def add_all_seasons_for_player(self, conn, player, base_data):
    for year_stats in player["seasonTotals"]:
      if (
          year_stats["gameTypeId"] == 2 and
          year_stats["leagueAbbrev"] == "NHL"
      ):
          self.save_player_season(
              conn,
              base_data["id"],
              str(year_stats["season"]),
              {
                "goals": year_stats.get("goals"),
                "assists": year_stats.get("assists"),
                "shots": year_stats.get("shots"),
                "avg_toi": year_stats.get("avgToi"),
                "plus_minus": year_stats.get("plusMinus"),
                "games_played": year_stats.get("gamesPlayed"),
                "team": year_stats.get("teamName", {}).get("default"),
              }
          )

  def save_player_season(self, conn, player_id, season, stats):
    cur = conn.cursor()

    # check to make sure not added a duplicate season
    cur.execute("""
        SELECT 1
        FROM player_seasons
        WHERE player_id = ? AND season = ?
    """, (player_id, season))

    existing = cur.fetchone()

    if existing is None:
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

  def save_player(self, conn, data):
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO players (
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

  
p_fill = PlayerFill()
p_fill.add_players_by_year("20252026")