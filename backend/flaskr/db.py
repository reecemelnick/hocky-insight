import sqlite3
import click
import requests
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

@click.command("insert-team-elo")
@with_appcontext
def insert_elo_command():

    teams = [
        "Ducks", "Bruins", "Sabres", "Flames", "Hurricanes", "Blackhawks", "Avalanche",
        "Blue Jackets", "Stars", "Red Wings", "Oilers", "Panthers", "Kings", "Wild",
        "Canadiens", "Predators", "Devils", "Islanders", "Rangers", "Senators",
        "Flyers", "Penguins", "Sharks", "Kraken", "Blues", "Lightning", "Maple Leafs",
        "Mammoth", "Canucks", "Golden Knights", "Capitals", "Jets"
    ]   

    db = get_db()
    for team in teams:
        db.execute(
            """
            INSERT INTO elo (team_name, elo)
            VALUES (?, ?)       
            """,
            (team, 1500)
        )
    
    db.commit()
    click.echo("Team elo reset")     

@click.command("reset-elo")
@with_appcontext
def reset_elo_command():
    db = get_db()
    db.execute(
        "UPDATE elo SET elo = ?",
        (1500,)
    )
    
    db.commit()
    click.echo("Team elo reset")   

def reset_elo_helper():
    db = get_db()
    db.execute(
        "UPDATE elo SET elo = ?",
        (1500,)
    )
    
    db.commit()

@click.command("clear-last-date")
@with_appcontext
def clear_last_date_command():
    db = get_db()
    db.execute("DELETE FROM updates")
    db.commit()
    click.echo("Cleard last date")    

@click.command("backfill-20242025-seasons")
@with_appcontext
def backfill_20242025_seasons_command():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT player_id FROM player_predictions")
    player_ids = [row[0] for row in cursor.fetchall()]

    inserted = 0

    for player_id in player_ids:
        response = requests.get(f"https://api-web.nhle.com/v1/player/{player_id}/landing")
        response.raise_for_status()
        payload = response.json()

        player_info = {
            "name": f"{payload['firstName']['default']} {payload['lastName']['default']}",
            "country": payload.get("birthCountry"),
            "id": payload["playerId"],
            "height": payload.get("heightInInches"),
            "weight": payload.get("weightInPounds"),
            "birth_date": payload.get("birthDate"),
            "position": payload.get("position"),
        }

        db.execute(
            """
            INSERT OR REPLACE INTO players (
                player_id, name, country, height, weight, birth_date, position
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                player_info["id"],
                player_info["name"],
                player_info["country"],
                player_info["height"],
                player_info["weight"],
                player_info["birth_date"],
                player_info["position"],
            ),
        )

        season_stats = next(
            (
                season
                for season in payload.get("seasonTotals", [])
                if season.get("season") == 20242025
                and season.get("gameTypeId") == 2
                and season.get("leagueAbbrev") == "NHL"
            ),
            None,
        )

        if not season_stats:
            continue

        db.execute(
            "DELETE FROM player_seasons WHERE player_id = ? AND season = ?",
            (player_id, "20242025"),
        )
        db.execute(
            """
            INSERT INTO player_seasons (
                player_id, season,
                goals, assists, shots,
                plus_minus, games_played, avg_toi, team
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                player_id,
                "20242025",
                season_stats.get("goals"),
                season_stats.get("assists"),
                season_stats.get("shots"),
                season_stats.get("plusMinus"),
                season_stats.get("gamesPlayed"),
                season_stats.get("avgToi"),
                season_stats.get("teamName", {}).get("default"),
            ),
        )
        inserted += 1

    db.commit()
    click.echo(f"Backfilled 20242025 season stats for {inserted} players")

@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")