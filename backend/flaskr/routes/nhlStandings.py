from flask import Blueprint, request
from ..services.nhlStandings import StandingsManager 

bp = Blueprint("standings", __name__)

standings_manager = StandingsManager()

@bp.route("/standings", methods=["GET"])
def standings():
    standings_data = standings_manager.get_standings()
    return standings_data, 200

# help with office pools