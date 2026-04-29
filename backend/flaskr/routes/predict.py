from flask import jsonify, Blueprint, request
import os
import joblib
import pandas as pd
from ..services.player_data import process_data, generate_team_csv

bp = Blueprint("predict", __name__)

BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "..", "data", "nhl_ppg_model.pkl")
model = joblib.load(model_path)
scaler_path = os.path.join(BASE_DIR, "..", "data", "scaler_params.pkl")
scaler = joblib.load(scaler_path)

# passed in example
team_code = "VAN"

# def make_team_csv(team_code):
#         print(team_code)


@bp.route("/predict", methods=["GET"])
def predict():

    # generate_team_csv("VAN")
    # csv_path = os.path.join(BASE_DIR, "..", "data", "canucks.csv")
    # df = process_data(csv_path)

    # names = df["name"]
    # X = df.drop(columns=["name"])

    # X = pd.get_dummies(X, columns=["position"])
    # X = X.reindex(columns=model.feature_names_in_, fill_value=0)

    # for col in scaler:
    #     if col in X:
    #         X[col] = (X[col] - scaler[col]["mu"]) / scaler[col]["sig"]

    # preds = model.predict(X)

    # result = [
    #     {"name": n, "ppg": float(p)}
    #     for n, p in zip(names, preds)
    # ]
    result = "success"
    return jsonify(result)