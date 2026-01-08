from flask import Blueprint, request
from ..services.scores import ScoreManager 

bp = Blueprint("scores", __name__, url_prefix="/scores")

score_manager = ScoreManager() 
    
# a simple page that give todays scores
@bp.route("", methods=["GET"])
def scores():
    date = request.args.get("date")
    if date is None:
        return {"error": "date is required"}, 400
    
    score_data = score_manager.get_scores_specific_date(date)
    # no games played on this date
    if score_data is None:
        return [], 200

    return score_data, 200 # games were played on this date