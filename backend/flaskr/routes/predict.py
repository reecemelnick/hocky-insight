from flask import jsonify, Blueprint, request
from ..db import get_db

bp = Blueprint("predict", __name__)
@bp.route("/predict", methods=["GET"])
def predict():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            pp.player_id,
            pp.name,
            pp.predicted_ppg,
            ps.goals,
            ps.assists,
            ps.games_played
        FROM player_predictions pp
        LEFT JOIN player_seasons ps
            ON pp.player_id = ps.player_id
            AND ps.season = '20242025'
        ORDER BY pp.predicted_ppg DESC
    """)

    rows = cursor.fetchall()

    result = [
        {
            "player_id": r[0],
            "name": r[1],
            "ppg": ((r[3] + r[4]) / r[5]) if r[5] else None,
            "predicted_ppg": r[2]
        }
        for r in rows
    ]

    return jsonify(result)
    