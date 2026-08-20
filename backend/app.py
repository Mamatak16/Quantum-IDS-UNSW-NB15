import os
import sys

# Ensure project root & backend dir are at top of sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from utils.logger import logger
from utils.security import rate_limit_middleware, apply_security_headers
from utils.response import make_response, make_error
from services.model_service import model_service
from routes.predict_routes import predict_bp
from routes.analytics_routes import analytics_bp
from routes.xai_routes import xai_bp
from routes.export_routes import export_bp

def create_app():
    app = Flask(
        __name__,
        static_folder="../frontend/dist",
        static_url_path=""
    )

    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3001", "http://127.0.0.1:3001", "http://localhost:5174", "http://127.0.0.1:5174", "*"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    app.before_request(rate_limit_middleware)
    app.after_request(apply_security_headers)

    app.register_blueprint(predict_bp, url_prefix="/api/v1")
    app.register_blueprint(analytics_bp, url_prefix="/api/v1")
    app.register_blueprint(xai_bp, url_prefix="/api/v1")
    app.register_blueprint(export_bp, url_prefix="/api/v1")

    @app.route("/api/health", methods=["GET"])
    @app.route("/api/v1/health", methods=["GET"])
    def api_health():
        status = model_service.get_models_status()
        return jsonify({
            "status": "ok",
            "service": "Quantum IDS API (UNSW-NB15)",
            "dataset": "UNSW-NB15",
            "models_loaded": status
        })

    @app.route("/", methods=["GET"])
    def index():
        if os.path.exists(app.static_folder) and os.path.exists(os.path.join(app.static_folder, "index.html")):
            return send_from_directory(app.static_folder, "index.html")
        status = model_service.get_models_status()
        return jsonify({
            "status": "online",
            "system": "Quantum Intrusion Detection System (UNSW-NB15)",
            "dataset": "UNSW-NB15",
            "models_loaded": status
        })

    @app.route("/model-info", methods=["GET"])
    def model_info():
        return jsonify({
            "dataset": "UNSW-NB15",
            "pca_components": 4,
            "models": ["Classical SVM (RBF)", "Quantum SVM (ZFeatureMap)", "Variational Quantum Classifier (VQC)"],
            "feature_map": "ZFeatureMap (4 Qubits)",
            "optimizer": "COBYLA / SPSA",
            "description": "Hybrid quantum-classical intrusion detection platform specifically adapted for UNSW-NB15 network telemetry."
        })

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting Quantum-IDS UNSW-NB15 Backend Server on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
