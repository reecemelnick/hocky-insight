import sqlite3
import click
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

@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")