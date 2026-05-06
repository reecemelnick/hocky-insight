from flask import Blueprint, request
from ..services.ppg_predict_retreiver import PpgPredictRetriever

bp = Blueprint("predict", __name__)
ppg_retriever = PpgPredictRetriever()
# example: /api/predict?page=2

@bp.route("/predict", methods=["GET"])
def predict():
    page = int(request.args.get("page", 1))
    result = ppg_retriever.get_ppg_predictions(page)
    return result, 200
    