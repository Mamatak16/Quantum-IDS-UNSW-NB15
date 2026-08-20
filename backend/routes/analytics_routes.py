from flask import Blueprint
from services.model_service import model_service
from utils.response import make_response

analytics_bp = Blueprint("analytics_bp", __name__)

@analytics_bp.route("/analytics/stats", methods=["GET"])
def get_stats():
    return make_response({
        "dataset": {
            "name": "UNSW-NB15 Benchmark",
            "features_pca": 4,
            "training_samples": 175341,
            "test_samples": 82332,
            "attack_categories": [
                "Normal", "Fuzzers", "Analysis", "Backdoors", "DoS",
                "Exploits", "Generic", "Reconnaissance", "Shellcode", "Worms"
            ]
        },
        "models_summary": [
            {
                "id": "svm",
                "name": "Classical SVM (RBF Kernel)",
                "accuracy": 94.20,
                "precision": 93.80,
                "recall": 94.50,
                "f1_score": 94.15,
                "macro_f1": 92.80,
                "training_time_sec": 6.8,
                "inference_time_ms": 0.15,
                "advantages": ["Fast execution latency", "Deterministic RBF decision boundaries"],
                "limitations": ["Quadratic training memory", "Fixed non-quantum distance kernel"]
            },
            {
                "id": "qsvm_z",
                "name": "Quantum SVM (ZFeatureMap)",
                "accuracy": 93.80,
                "precision": 93.10,
                "recall": 93.90,
                "f1_score": 93.50,
                "macro_f1": 92.10,
                "training_time_sec": 52.4,
                "inference_time_ms": 16.2,
                "advantages": ["Maps 4D PCA features to 2^4 = 16-dim Hilbert space", "Statevector fidelity inner product"],
                "limitations": ["Requires quantum state simulation", "Noisy gate execution on real QPUs"]
            },
            {
                "id": "vqc_base",
                "name": "VQC Baseline",
                "accuracy": 70.50,
                "precision": 69.80,
                "recall": 71.20,
                "f1_score": 70.49,
                "macro_f1": 69.10,
                "training_time_sec": 135.0,
                "inference_time_ms": 48.0,
                "advantages": ["Parameterized quantum circuit", "End-to-end quantum neural classifier"],
                "limitations": ["Unbounded StandardScaler causes phase aliasing", "COBYLA local optimizer stalling"]
            },
            {
                "id": "vqc_opt",
                "name": "VQC Optimized",
                "accuracy": 88.50,
                "precision": 87.90,
                "recall": 89.10,
                "f1_score": 88.49,
                "macro_f1": 87.20,
                "training_time_sec": 185.0,
                "inference_time_ms": 42.0,
                "advantages": ["MinMaxScaler (0..2pi) bounded angle scaling", "EfficientSU2 ansatz + COBYLA-250"],
                "limitations": ["Higher variational parameter optimization depth", "Simulator execution overhead"]
            }
        ],
        "vqc_improvement": {
            "baseline_accuracy": 70.50,
            "optimized_accuracy": 88.50,
            "improvement_pct_points": 18.00
        },
        "confusion_matrix": {
            "total_test": 1500,
            "tp": 680,
            "fp": 85,
            "fn": 88,
            "tn": 647
        }
    }, message="UNSW-NB15 analytics stats retrieved successfully")

@analytics_bp.route("/analytics/models", methods=["GET"])
def get_models_info():
    status = model_service.get_models_status()
    return make_response({
        "models_loaded": status,
        "dataset": "UNSW-NB15",
        "feature_map": "ZFeatureMap (4 Qubits)",
        "pca_components": 4,
        "quantum_backend": "Qiskit Aer Simulator (StatevectorSampler)"
    }, message="UNSW-NB15 model info retrieved successfully")
