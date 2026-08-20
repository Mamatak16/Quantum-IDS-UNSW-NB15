import time
import joblib
import numpy as np
from sklearn.svm import SVC
import qiskit
from qiskit.circuit.library import ZFeatureMap, ZZFeatureMap
from src.evaluation.metrics import evaluate_classification

try:
    from qiskit.primitives import StatevectorSampler as Sampler
except ImportError:
    try:
        from qiskit.primitives import Sampler
    except ImportError:
        Sampler = None

class QSVMModel:
    def __init__(self, num_qubits=4, feature_map_type="z", reps=1, C=1.0):
        self.num_qubits = num_qubits
        self.feature_map_type = feature_map_type
        self.reps = reps
        self.C = C

        if feature_map_type == "zz":
            self.feature_map = ZZFeatureMap(feature_dimension=num_qubits, reps=reps, entanglement="linear")
        else:
            self.feature_map = ZFeatureMap(feature_dimension=num_qubits, reps=reps)

        self.svc = SVC(kernel="precomputed", C=C, random_state=42)
        self.X_train_ref = None
        self.training_time_sec = 0.0

    def _compute_quantum_kernel(self, X1, X2):
        """Computes statevector fidelity kernel matrix between X1 and X2."""
        from qiskit.quantum_info import Statevector
        
        # Bind features and compute statevectors
        def get_statevectors(X):
            svs = []
            for sample in X:
                bound_circuit = self.feature_map.assign_parameters(sample)
                svs.append(Statevector.from_instruction(bound_circuit))
            return svs

        svs1 = get_statevectors(X1)
        svs2 = get_statevectors(X2) if X1 is not X2 else svs1

        # Calculate inner product overlap fidelity |<psi1|psi2>|^2
        kernel_matrix = np.zeros((len(X1), len(X2)))
        for i, sv1 in enumerate(svs1):
            for j, sv2 in enumerate(svs2):
                if X1 is X2 and j < i:
                    kernel_matrix[i, j] = kernel_matrix[j, i]
                else:
                    fidelity = abs(sv1.inner(sv2)) ** 2
                    kernel_matrix[i, j] = fidelity

        return kernel_matrix

    def fit(self, X_train, y_train):
        start = time.time()
        self.X_train_ref = np.copy(X_train)
        K_train = self._compute_quantum_kernel(X_train, X_train)
        self.svc.fit(K_train, y_train)
        self.training_time_sec = round(time.time() - start, 2)
        return self

    def predict(self, X_test):
        K_test = self._compute_quantum_kernel(X_test, self.X_train_ref)
        return self.svc.predict(K_test)

    def evaluate(self, X_test, y_test):
        start = time.time()
        y_pred = self.predict(X_test)
        pred_time = round((time.time() - start) / max(len(X_test), 1) * 1000, 3)
        metrics = evaluate_classification(y_test, y_pred)
        metrics["training_time_sec"] = self.training_time_sec
        metrics["prediction_time_ms"] = pred_time
        return metrics

    def save(self, filepath):
        bundle = {
            "model": self.svc,
            "X_train": self.X_train_ref,
            "num_qubits": self.num_qubits,
            "feature_map_type": self.feature_map_type,
            "reps": self.reps
        }
        joblib.dump(bundle, filepath)
