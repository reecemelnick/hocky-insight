from flask import Blueprint, request
from ..services.ppg_predict_retreiver import PpgPredictRetriever

bp = Blueprint("predict", __name__)
ppg_retriever = PpgPredictRetriever()
# example: /api/predict?page=2

@bp.route("/predict", methods=["GET"])
def predict():
    page = int(request.args.get("page", 1))
    season = request.args.get("season", "20262027")
    sort_by = request.args.get("sort", "predicted_ppg")
    order = request.args.get("order", "DESC")
    position = request.args.get("position", "all")
    result = ppg_retriever.get_ppg_predictions(page, season, sort_by, order, position)
    return result, 200
    