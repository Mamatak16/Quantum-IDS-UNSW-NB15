import os
import time
import joblib
import numpy as np
import qiskit
from qiskit.circuit.library import ZFeatureMap, ZZFeatureMap, RealAmplitudes, EfficientSU2
from qiskit_algorithms.optimizers import COBYLA, SPSA, L_BFGS_B
from qiskit_machine_learning.algorithms import VQC

try:
    from qiskit.primitives import StatevectorSampler as Sampler
except ImportError:
    try:
        from qiskit.primitives import Sampler
    except ImportError:
        Sampler = None

from src.evaluation.metrics import evaluate_classification

# Top-level named interpret parity function (Pickle-safe)
def global_parity(x: int) -> int:
    return bin(x).count("1") % 2

class FitResult:
    """Lightweight fit result container for Qiskit VQC weight restoration."""
    def __init__(self, x):
        self.x = np.array(x)
        self.success = True

class VQCModel:
    def __init__(
        self,
        num_qubits=4,
        feature_map_type="z",
        fm_reps=1,
        ansatz_type="real_amplitudes",
        ansatz_reps=2,
        entanglement="full",
        optimizer_type="cobyla",
        maxiter=200
    ):
        self.num_qubits = num_qubits
        self.feature_map_type = feature_map_type
        self.fm_reps = fm_reps
        self.ansatz_type = ansatz_type
        self.ansatz_reps = ansatz_reps
        self.entanglement = entanglement
        self.optimizer_type = optimizer_type
        self.maxiter = maxiter

        # 1. Feature Map
        if feature_map_type == "zz_full":
            self.feature_map = ZZFeatureMap(feature_dimension=num_qubits, reps=fm_reps, entanglement="full")
        elif feature_map_type == "zz_linear":
            self.feature_map = ZZFeatureMap(feature_dimension=num_qubits, reps=fm_reps, entanglement="linear")
        else:
            self.feature_map = ZFeatureMap(feature_dimension=num_qubits, reps=fm_reps)

        # 2. Ansatz
        if ansatz_type == "efficient_su2":
            self.ansatz = EfficientSU2(num_qubits=num_qubits, reps=ansatz_reps, entanglement=entanglement)
        else:
            self.ansatz = RealAmplitudes(num_qubits=num_qubits, reps=ansatz_reps, entanglement=entanglement)

        # 3. Optimizer (set min maxiter to avoid scipy warnings)
        eff_maxiter = max(maxiter, 20)
        if optimizer_type == "spsa":
            self.optimizer = SPSA(maxiter=eff_maxiter)
        elif optimizer_type == "l_bfgs_b":
            self.optimizer = L_BFGS_B(maxiter=eff_maxiter)
        else:
            self.optimizer = COBYLA(maxiter=eff_maxiter)

        vqc_kwargs = {
            "feature_map": self.feature_map,
            "ansatz": self.ansatz,
            "optimizer": self.optimizer,
            "interpret": global_parity
        }
        if Sampler is not None:
            try:
                vqc_kwargs["sampler"] = Sampler()
            except Exception:
                pass

        self.vqc = VQC(**vqc_kwargs)
        self.training_time_sec = 0.0

    def fit(self, X_train, y_train):
        start = time.time()
        self.vqc.fit(X_train, y_train)
        self.training_time_sec = round(time.time() - start, 2)
        return self

    def predict(self, X):
        return self.vqc.predict(X)

    def evaluate(self, X_test, y_test):
        start = time.time()
        y_pred = self.predict(X_test)
        pred_time = round((time.time() - start) / max(len(X_test), 1) * 1000, 3)
        metrics = evaluate_classification(y_test, y_pred)
        metrics["training_time_sec"] = self.training_time_sec
        metrics["prediction_time_ms"] = pred_time
        return metrics

    def save_bundle(self, filepath, scaler=None, pca=None, metrics=None):
        """Saves pickle-safe lightweight model bundle containing trained weights and configuration."""
        weights = np.array(self.vqc.weights) if hasattr(self.vqc, "weights") and self.vqc.weights is not None else None
        classes = np.array(self.vqc.classes_) if hasattr(self.vqc, "classes_") and self.vqc.classes_ is not None else np.array([0, 1])

        bundle = {
            "weights": weights,
            "classes": classes,
            "scaler": scaler,
            "pca": pca,
            "metrics": metrics,
            "config": {
                "num_qubits": self.num_qubits,
                "feature_map_type": self.feature_map_type,
                "fm_reps": self.fm_reps,
                "ansatz_type": self.ansatz_type,
                "ansatz_reps": self.ansatz_reps,
                "entanglement": self.entanglement,
                "optimizer_type": self.optimizer_type,
                "maxiter": self.maxiter
            }
        }
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(bundle, filepath)
        return bundle

    @classmethod
    def load_from_bundle(cls, bundle_or_filepath):
        """Reconstructs VQC model from pickle-safe saved bundle."""
        if isinstance(bundle_or_filepath, str):
            bundle = joblib.load(bundle_or_filepath)
        else:
            bundle = bundle_or_filepath

        config = bundle.get("config", {})
        model_obj = cls(
            num_qubits=config.get("num_qubits", 4),
            feature_map_type=config.get("feature_map_type", "z"),
            fm_reps=config.get("fm_reps", 1),
            ansatz_type=config.get("ansatz_type", "real_amplitudes"),
            ansatz_reps=config.get("ansatz_reps", 2),
            entanglement=config.get("entanglement", "full"),
            optimizer_type=config.get("optimizer_type", "cobyla"),
            maxiter=config.get("maxiter", 200)
        )

        weights = bundle.get("weights")
        classes = bundle.get("classes", np.array([0, 1]))

        if weights is not None:
            # Fit on dummy sample to initialize internal QNN circuit structure
            dummy_X = np.zeros((len(classes), model_obj.num_qubits))
            dummy_y = classes
            model_obj.vqc.fit(dummy_X, dummy_y)
            # Restore exact trained weights via _fit_result container
            model_obj.vqc._fit_result = FitResult(weights)

        return model_obj
