from flask import Blueprint
from ..services.ppg_predict_retreiver import PpgPredictRetriever

bp = Blueprint("predict", __name__)
ppg_retriever = PpgPredictRetriever()

@bp.route("/predict", methods=["GET"])
def predict():
    result = ppg_retriever.get_ppg_predictions()
    return result, 200
    