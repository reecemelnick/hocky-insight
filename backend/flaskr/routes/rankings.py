from flask import Blueprint, jsonify
from ..services.rankings import RankingManager

bp = Blueprint("rankings", __name__)

ranking_manager = RankingManager()

@bp.route("/rankings", methods=["GET"])
def rankings():
    ranking_data = ranking_manager.get_ranked_teams()
    return jsonify(ranking_data), 200