

CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    home_score INTEGER,
    away_score INTEGER
);

CREATE TABLE IF NOT EXISTS elo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT UNIQUE NOT NULL,
    elo INTEGER
);

CREATE TABLE IF NOT EXISTS updates (
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

DROP TABLE IF EXISTS player_predictions;
CREATE TABLE IF NOT EXISTS player_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    name TEXT,
    predicted_ppg REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);