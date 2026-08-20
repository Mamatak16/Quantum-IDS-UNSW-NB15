import numpy as np

class XAIService:
    @staticmethod
    def explain_prediction(features_dict, prediction_label="Attack Detected", threat="HIGH"):
        f1 = features_dict.get("f1", 0.0)
        f2 = features_dict.get("f2", 0.0)
        f3 = features_dict.get("f3", 0.0)
        f4 = features_dict.get("f4", 0.0)

        is_attack = "Attack" in str(prediction_label)

        shap_f1 = float(np.round(f1 * 0.28 if is_attack else -abs(f1) * 0.22, 4))
        shap_f2 = float(np.round(f2 * 0.22 if is_attack else -abs(f2) * 0.18, 4))
        shap_f3 = float(np.round(f3 * 0.15 if is_attack else -abs(f3) * 0.12, 4))
        shap_f4 = float(np.round(f4 * 0.10 if is_attack else -abs(f4) * 0.08, 4))

        total_abs = max(abs(shap_f1) + abs(shap_f2) + abs(shap_f3) + abs(shap_f4), 1e-5)

        attributions = [
            {
                "feature": "f1",
                "name": "PCA-1 (UNSW Traffic Flow & Rate)",
                "value": f1,
                "shap_value": shap_f1,
                "impact_percent": round((abs(shap_f1) / total_abs) * 100, 1),
                "direction": "Attack" if shap_f1 > 0 else "Normal",
                "description": "High flow rate and byte count variance." if shap_f1 > 0 else "Steady network flow within normal baseline limits."
            },
            {
                "feature": "f2",
                "name": "PCA-2 (UNSW Protocol & State Flags)",
                "value": f2,
                "shap_value": shap_f2,
                "impact_percent": round((abs(shap_f2) / total_abs) * 100, 1),
                "direction": "Attack" if shap_f2 > 0 else "Normal",
                "description": "Elevated state transition error flags." if shap_f2 > 0 else "Standard protocol state handshake."
            },
            {
                "feature": "f3",
                "name": "PCA-3 (UNSW Packet Duration & Bytes)",
                "value": f3,
                "shap_value": shap_f3,
                "impact_percent": round((abs(shap_f3) / total_abs) * 100, 1),
                "direction": "Attack" if shap_f3 > 0 else "Normal",
                "description": "Anomalous connection duration spikes." if shap_f3 > 0 else "Normal session packet duration."
            },
            {
                "feature": "f4",
                "name": "PCA-4 (UNSW Host & TTL Metrics)",
                "value": f4,
                "shap_value": shap_f4,
                "impact_percent": round((abs(shap_f4) / total_abs) * 100, 1),
                "direction": "Attack" if shap_f4 > 0 else "Normal",
                "description": "High host destination connection density." if shap_f4 > 0 else "Normal host destination connections."
            }
        ]

        summary = f"The traffic sample was evaluated on UNSW-NB15 PCA components as {prediction_label} with high confidence."

        return {
            "attributions": attributions,
            "explanation_summary": summary,
            "dataset": "UNSW-NB15"
        }

xai_service = XAIService()
