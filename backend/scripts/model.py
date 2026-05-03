

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, root_mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os
import re
from player_data import process_data, get_sqlite_conn, get_eligible_players, get_prediction_dataframe
from collections import defaultdict


def normalize_data(data):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scaler_path = os.path.join(BASE_DIR, "scaler_params.pkl")
    standardization = joblib.load(scaler_path)
    for col in ["height", "plus_minus_1", "plus_minus_2", "avg_toi_1", "avg_toi_2", "weight", "age"]:
        data[col] = (data[col] - standardization[col]["mu"]) / standardization[col]["sig"]
    return data

def train_model():

    df = pd.read_csv('player_final.csv')

    X = df.drop(['ppg_3'], axis=1)
    Y = df['ppg_3']

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.15)

    print('Number of training data:', len(x_train))
    print('Number of testing data:', len(x_test))

    standardization = {}
    for col in ["height", "plus_minus_1", "plus_minus_2", "avg_toi_1", "avg_toi_2", "weight", "age"]:
        mu = x_train[col].mean()
        sig = x_train[col].std()
        standardization[col] = {"mu": mu, "sig": sig} 

    x_train = normalize_data(x_train)
    x_test = normalize_data(x_test)

    model = LinearRegression().fit(x_train, y_train)
    joblib.dump(model, 'nhl_ppg_model.pkl')
    joblib.dump(standardization, 'scaler_params.pkl')

def get_prediction_table_name(prediction_season):
    season = str(prediction_season)
    if not re.fullmatch(r"\d{8}", season):
        raise ValueError(f"Invalid season format: {prediction_season}. Expected YYYYYYYY.")
    return f"player_predictions_{season}"

def ensure_prediction_table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            name TEXT,
            predicted_ppg REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

def save_predictions(conn, predictions, prediction_season):
    cursor = conn.cursor()
    table_name = get_prediction_table_name(prediction_season)

    ensure_prediction_table(conn, table_name)

    cursor.execute(f"DELETE FROM {table_name}")

    for _, row in predictions.iterrows():
        cursor.execute(f"""
            INSERT INTO {table_name} (player_id, name, predicted_ppg)
            VALUES (?, ?, ?)
        """, (
            int(row["player_id"]),
            row["name"],
            float(row["ppg"])
        ))

    conn.commit()

def get_all_predictions(conn, prediction_season=None):
    cursor = conn.cursor()
    table_name = "player_predictions"
    if prediction_season is not None:
        table_name = get_prediction_table_name(prediction_season)

    cursor.execute(f"""
        SELECT player_id, name, predicted_ppg
        FROM {table_name}
        ORDER BY predicted_ppg DESC
    """)

    rows = cursor.fetchall()

    return [
        {
            "player_id": row[0],
            "name": row[1],
            "ppg": row[2]
        }
        for row in rows
    ]

# format previous season: eg 20232024 -> 20222023 when passed in 1 as arg 2
def get_prev_season(season, years_ago):
    year1 = int(season[:4]) - years_ago
    year2 = int(season[4:]) - years_ago
    return f"{year1}{year2}"

def load_prediction_players(conn, prediction_season):
    cur = conn.cursor()
    
    prev_season1 = get_prev_season(prediction_season, 1)
    prev_season2 = get_prev_season(prediction_season, 2)

    cur.execute("""
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
        WHERE s.season IN (?, ?)
        ORDER BY p.player_id, s.season
    """, (prev_season1, prev_season2))

    rows = cur.fetchall()

    return rows

def build_player_dict(rows):
    players = defaultdict(dict)

    for r in rows:
        pid = r["player_id"]
        season = r["season"]

        players[pid]["player_id"] = pid
        players[pid]["name"] = r["name"]
        players[pid]["height"] = r["height"]
        players[pid]["weight"] = r["weight"]
        players[pid]["birth_date"] = r["birth_date"]
        players[pid]["position"] = r["position"]

        players[pid][season] = {
            "goals": r["goals"],
            "assists": r["assists"],
            "shots": r["shots"],
            "avg_toi": r["avg_toi"],
            "plus_minus": r["plus_minus"],
            "games_played": r["games_played"],
        }

    return list(players.values())

def get_prediction_data(players, prediction_season):
    pred_data = []

    prev_season1 = get_prev_season(prediction_season, 1)
    prev_season2 = get_prev_season(prediction_season, 2)

    for p in players:

        # must have BOTH seasons
        if prev_season1 not in p or prev_season2 not in p:
            continue

        data = {
            "player_id": p["player_id"],
            "name": p["name"],
            "height": p["height"],
            "weight": p["weight"],
            "birth_date": p["birth_date"],
            "position": p["position"],
        }

        data.update({
            "goals_1": p[prev_season1]["goals"],
            "assists_1": p[prev_season1]["assists"],
            "shots_1": p[prev_season1]["shots"],
            "avg_toi_1": p[prev_season1]["avg_toi"],
            "plus_minus_1": p[prev_season1]["plus_minus"],
            "games_played_1": p[prev_season1]["games_played"],

            "goals_2": p[prev_season2]["goals"],
            "assists_2": p[prev_season2]["assists"],
            "shots_2": p[prev_season2]["shots"],
            "avg_toi_2": p[prev_season2]["avg_toi"],
            "plus_minus_2": p[prev_season2]["plus_minus"],
            "games_played_2": p[prev_season2]["games_played"],
        })

        data["season_3"] = prediction_season

        pred_data.append(data)

    return pred_data

def predict_year_ppg(season_to_predict):
    conn = get_sqlite_conn()

    rows = load_prediction_players(conn, season_to_predict)
  
    players = build_player_dict(rows)

    df = pd.DataFrame(get_prediction_data(players, season_to_predict))
    # print(df)

    df = process_data(df)

    df_pred_final = df[["player_id", "name","games_played_1", "games_played_2", "goals_1", "goals_2",
                "height", "plus_minus_1", "plus_minus_2", "position",
                "shots_1", "shots_2", "avg_toi_1", "avg_toi_2",
                "weight", "points_1", "points_2", "age"]]

    meta = df_pred_final[["player_id", "name"]].copy()
    X = df_pred_final.drop(columns=["player_id", "name"])

    positions = ["C", "L", "R", "D"]
    df_pred_final["position"] = pd.Categorical(
        df_pred_final["position"],
        categories=positions
    )

    df_pred_final = pd.get_dummies(df_pred_final, columns=["position"])

    df_pred_final = normalize_data(df_pred_final)

    cols = ['games_played_1', 'games_played_2', 'goals_1', 'goals_2', 'height',
       'plus_minus_1', 'plus_minus_2', 'shots_1', 'shots_2', 'avg_toi_1',
       'avg_toi_2', 'weight', 'points_1', 'points_2', 'age', 'position_C',
       'position_D', 'position_L', 'position_R']
    
    df_pred_final = df_pred_final.reindex(
        columns=cols,
        fill_value=0
    )

    print(df_pred_final)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(BASE_DIR, "nhl_ppg_model.pkl")
    model = joblib.load(model_path)
    pred_ppg = model.predict(df_pred_final)

    predictions = pd.DataFrame({
        "player_id": meta["player_id"].values,
        "name": meta["name"].values,
        "ppg": pred_ppg
    })

    predictions[["first_name", "last_name"]] = predictions["name"].str.split(" ", n=1, expand=True)

    save_predictions(conn, predictions, season_to_predict)

    print(predictions.sort_values(by="ppg"))

# predict_year_ppg("20192020")

