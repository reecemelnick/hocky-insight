from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, root_mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from player_data import process_data, get_sqlite_conn, get_eligible_players, get_prediction_dataframe
from collections import defaultdict

df = pd.read_csv('player_final.csv')

# X is all columns no ppg_3
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

def normalize_data(data):
    for col in ["height", "plus_minus_1", "plus_minus_2", "avg_toi_1", "avg_toi_2", "weight", "age"]:
        data[col] = (data[col] - standardization[col]["mu"]) / standardization[col]["sig"]
    return data 

x_train = normalize_data(x_train)
x_test = normalize_data(x_test)

model = LinearRegression().fit(x_train, y_train)
joblib.dump(model, 'nhl_ppg_model.pkl')
joblib.dump(standardization, 'scaler_params.pkl')

def predict_all_players():
    conn = get_sqlite_conn()

    ids = get_eligible_players()

    df = get_prediction_dataframe(conn, ids)
    print(df)
    df = process_data(df)
    print("after process")

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

    df_pred_final = df_pred_final.reindex(
        columns=x_train.columns,
        fill_value=0
    )

    print(df_pred_final)

    pred_ppg = model.predict(df_pred_final)

    predictions = pd.DataFrame({
        "player_id": meta["player_id"].values,
        "name": meta["name"].values,
        "ppg": pred_ppg
    })

    predictions[["first_name", "last_name"]] = predictions["name"].str.split(" ", n=1, expand=True)

    save_predictions(conn, predictions)

    print(predictions.sort_values(by="ppg"))

def save_predictions(conn, predictions):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM player_predictions")

    for _, row in predictions.iterrows():
        cursor.execute("""
            INSERT INTO player_predictions (player_id, name, predicted_ppg)
            VALUES (?, ?, ?)
        """, (
            int(row["player_id"]),
            row["name"],
            float(row["ppg"])
        ))

    conn.commit()

def get_all_predictions(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT player_id, name, predicted_ppg
        FROM player_predictions
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


def load_prediction_players(conn):
    cur = conn.cursor()

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
        WHERE s.season IN ('20222023', '20232024')
        ORDER BY p.player_id, s.season
    """)

    rows = cur.fetchall()

    return rows

def build_player_dict(rows):
    players = defaultdict(dict)

    for r in rows:
        pid = r[0]
        season = r[6]

        players[pid]["player_id"] = pid
        players[pid]["name"] = r[1]
        players[pid]["height"] = r[2]
        players[pid]["weight"] = r[3]
        players[pid]["birth_date"] = r[4]
        players[pid]["position"] = r[5]

        players[pid][season] = {
            "goals": r[7],
            "assists": r[8],
            "shots": r[9],
            "avg_toi": r[10],
            "plus_minus": r[11],
            "games_played": r[12],
        }

    return list(players.values())

def get_prediction_data(players):
    pred_data = []

    for p in players:

        # must have BOTH seasons
        if "20222023" not in p or "20232024" not in p:
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
            "goals_1": p["20222023"]["goals"],
            "assists_1": p["20222023"]["assists"],
            "shots_1": p["20222023"]["shots"],
            "avg_toi_1": p["20222023"]["avg_toi"],
            "plus_minus_1": p["20222023"]["plus_minus"],
            "games_played_1": p["20222023"]["games_played"],

            "goals_2": p["20232024"]["goals"],
            "assists_2": p["20232024"]["assists"],
            "shots_2": p["20232024"]["shots"],
            "avg_toi_2": p["20232024"]["avg_toi"],
            "plus_minus_2": p["20232024"]["plus_minus"],
            "games_played_2": p["20232024"]["games_played"],
        })

        # IMPORTANT: this is just a label (not used in training input)
        data["season_3"] = "20242025"

        pred_data.append(data)

    return pred_data

def predict_20242025():
    conn = get_sqlite_conn()

    rows = load_prediction_players(conn)
    players = build_player_dict(rows)

    df = pd.DataFrame(get_prediction_data(players))

    print(df)

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

    df_pred_final = df_pred_final.reindex(
        columns=x_train.columns,
        fill_value=0
    )

    print(df_pred_final)

    pred_ppg = model.predict(df_pred_final)

    predictions = pd.DataFrame({
        "player_id": meta["player_id"].values,
        "name": meta["name"].values,
        "ppg": pred_ppg
    })

    predictions[["first_name", "last_name"]] = predictions["name"].str.split(" ", n=1, expand=True)

    save_predictions(conn, predictions)

    print(predictions.sort_values(by="ppg"))

print(get_all_predictions(get_sqlite_conn()))
