from flask import Blueprint, request
from ..services.rankings import RankingManager

bp = Blueprint("rankings", __name__)

ranking_manager = RankingManager()

@bp.route("/rankings", methods=["GET"])
def rankings():
    ranking_data = ranking_manager.get_ranked_teams()
    return ranking_data, 200