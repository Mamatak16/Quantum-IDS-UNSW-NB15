from flask import Blueprint, request, Response
from services.report_service import report_service
from utils.response import make_response, make_error

export_bp = Blueprint("export_bp", __name__)

@export_bp.route("/export/csv", methods=["POST"])
def export_csv():
    data = request.get_json(silent=True) or {}
    history = data.get("history", [])
    if not isinstance(history, list):
        return make_error("History must be a JSON array", 400)

    csv_data = report_service.generate_csv_report(history)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=unsw_nb15_prediction_history.csv"}
    )

@export_bp.route("/export/pdf-data", methods=["POST"])
def pdf_data():
    data = request.get_json(silent=True) or {}
    record = data.get("record", {})
    xai = data.get("explanation")
    if not record:
        return make_error("Prediction record data is required", 400)

    pdf_summary = report_service.prepare_pdf_summary(record, xai)
    return make_response(pdf_summary, message="UNSW-NB15 PDF summary prepared successfully")
