from flask import Blueprint, request
from services.model_service import model_service
from utils.response import make_response, make_error

predict_bp = Blueprint("predict_bp", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    model_type = data.get("model", "svm")
    preset = data.get("preset")

    try:
        if preset:
            res = model_service.predict(model_type=model_type, preset=preset)
        else:
            f1 = data.get("f1", 0.0)
            f2 = data.get("f2", 0.0)
            f3 = data.get("f3", 0.0)
            f4 = data.get("f4", 0.0)
            res = model_service.predict(model_type=model_type, features=[f1, f2, f3, f4])
        return make_response(res, message="Prediction completed successfully")
    except Exception as e:
        return make_error(str(e), 500)

@predict_bp.route("/predict/batch", methods=["POST"])
def predict_batch():
    # CSV batch upload prediction for UNSW-NB15
    file = request.files.get("file")
    model_type = request.form.get("model", "svm")

    if not file:
        return make_error("No file attachment provided", 400)

    try:
        import pandas as pd
        df = pd.read_csv(file)
        results = []
        normal_count = 0
        attack_count = 0

        for i, row in df.head(50).iterrows():
            f1 = float(row.get("f1", row.get("dur", 0.1)))
            f2 = float(row.get("f2", row.get("spkts", 1.0)))
            f3 = float(row.get("f3", row.get("sbytes", 64.0)))
            f4 = float(row.get("f4", row.get("rate", 10.0)))
            res = model_service.predict(model_type=model_type, features=[f1, f2, f3, f4])
            results.append(res)
            if res["prediction_code"] == 1:
                attack_count += 1
            else:
                normal_count += 1

        return make_response({
            "dataset": "UNSW-NB15",
            "total_processed": len(results),
            "normal_count": normal_count,
            "attack_count": attack_count,
            "predictions": results
        }, message="UNSW-NB15 CSV batch processing completed successfully")
    except Exception as e:
        return make_error(f"Failed to process CSV file: {e}", 400)
