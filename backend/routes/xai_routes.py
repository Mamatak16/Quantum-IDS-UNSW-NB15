from flask import Blueprint, request
from services.xai_service import xai_service
from utils.response import make_response, make_error

xai_bp = Blueprint("xai_bp", __name__)

@xai_bp.route("/xai/explain", methods=["POST"])
def explain():
    data = request.get_json(silent=True) or {}
    features = {
        "f1": float(data.get("f1", 0.0)),
        "f2": float(data.get("f2", 0.0)),
        "f3": float(data.get("f3", 0.0)),
        "f4": float(data.get("f4", 0.0))
    }
    prediction = data.get("prediction", "Attack Detected")
    threat = data.get("threat", "HIGH")

    explanation = xai_service.explain_prediction(features, prediction_label=prediction, threat=threat)
    return make_response(explanation, message="UNSW-NB15 SHAP XAI explanation calculated successfully")
