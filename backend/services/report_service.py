import io
import csv
from datetime import datetime

class ReportService:
    @staticmethod
    def generate_csv_report(predictions_list):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Timestamp", "Dataset", "Model", "Prediction", "Threat Level",
            "Confidence (%)", "Feature 1", "Feature 2", "Feature 3", "Feature 4"
        ])
        for record in predictions_list:
            features = record.get("features", {})
            writer.writerow([
                record.get("timestamp", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")),
                "UNSW-NB15",
                record.get("model_used", "svm").upper(),
                record.get("prediction", "Unknown"),
                record.get("threat", "NORMAL"),
                record.get("confidence", 88.0),
                features.get("f1", 0.0),
                features.get("f2", 0.0),
                features.get("f3", 0.0),
                features.get("f4", 0.0)
            ])
        return output.getvalue()

    @staticmethod
    def prepare_pdf_summary(prediction_record, xai_explanation=None):
        return {
            "report_id": f"UNSW-RPT-{int(datetime.utcnow().timestamp())}",
            "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "system_name": "Quantum Intrusion Detection System (UNSW-NB15)",
            "dataset": "UNSW-NB15 Benchmark (PCA-4 Feature Space)",
            "prediction_details": prediction_record,
            "explainability": xai_explanation
        }

report_service = ReportService()
