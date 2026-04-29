DROP TABLE IF EXISTS scores;

CREATE TABLE scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    home_score INTEGER,
    away_score INTEGER
);

DROP TABLE IF EXISTS elo;

CREATE TABLE elo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT UNIQUE NOT NULL,
    elo INTEGER
);

DROP TABLE IF EXISTS updates;

CREATE TABLE updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_update TEXT
);

CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT,
    height INTEGER,
    weight INTEGER,
    birth_date TEXT,
    position TEXT
);

CREATE TABLE IF NOT EXISTS player_seasons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    season TEXT,

    goals INTEGER,
    assists INTEGER,
    shots INTEGER,
    plus_minus INTEGER,
    games_played INTEGER,
    avg_toi TEXT,
    team TEXT,

    FOREIGN KEY(player_id) REFERENCES players(player_id)
);

CREATE TABLE IF NOT EXISTS player_ids (
    player_id INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS player_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    name TEXT,
    predicted_ppg REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);