import os
import sys
import numpy as np
import joblib

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models.vqc_model import VQCModel, global_parity
from src.models.classical_model import ClassicalSVMModel
from src.models.qsvm_model import QSVMModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
VQC_PKL = os.path.join(BACKEND_DIR, "vqc_model.pkl")

def test_serialization():
    print("==========================================================================")
    print("         VQC MODEL SERIALIZATION TEST (SAVE -> LOAD -> PREDICT)           ")
    print("==========================================================================")

    # 1. Instantiate and train a lightweight VQC
    print("\n1. Instantiating VQCModel with top-level global_parity interpret...")
    vqc_train = VQCModel(num_qubits=4, feature_map_type="z", fm_reps=1, ansatz_type="real_amplitudes", ansatz_reps=1, optimizer_type="cobyla", maxiter=20)
    
    X_train_dummy = np.random.uniform(0, 2*np.pi, size=(10, 4))
    y_train_dummy = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
    
    print("2. Fitting VQC on training samples...")
    vqc_train.fit(X_train_dummy, y_train_dummy)

    # 3. Save model bundle
    print(f"3. Saving pickle-safe VQC bundle to {VQC_PKL}...")
    bundle = vqc_train.save_bundle(VQC_PKL, scaler=None, pca=None, metrics={"accuracy": 53.33, "f1_score": 52.10})
    
    # 4. Verify file exists
    assert os.path.exists(VQC_PKL), "vqc_model.pkl was not created!"
    print(f"[OK] vqc_model.pkl created successfully ({os.path.getsize(VQC_PKL)} bytes)")

    # 5. Load model bundle in fresh context
    print("4. Loading VQC bundle from vqc_model.pkl...")
    loaded_bundle = joblib.load(VQC_PKL)
    reconstructed_vqc = VQCModel.load_from_bundle(loaded_bundle)
    print("[OK] VQCModel reconstructed successfully")

    # 6. Predict on sample input
    X_test_sample = np.random.uniform(0, 2*np.pi, size=(2, 4))
    preds = reconstructed_vqc.predict(X_test_sample)
    print(f"5. VQC Prediction test output on {X_test_sample.shape} samples: {preds}")

    # 7. Test Classical SVM & QSVM
    print("\n6. Testing Classical SVM & QSVM model wrappers...")
    svm = ClassicalSVMModel(C=1.0)
    svm.fit(X_train_dummy, y_train_dummy)
    svm_preds = svm.predict(X_test_sample)
    print(f"[OK] Classical SVM Prediction: {svm_preds}")

    qsvm = QSVMModel(num_qubits=4, feature_map_type="z")
    qsvm.fit(X_train_dummy, y_train_dummy)
    qsvm_preds = qsvm.predict(X_test_sample)
    print(f"[OK] QSVM Prediction: {qsvm_preds}")

    print("\n==========================================================================")
    print("         SERIALIZATION TEST COMPLETED SUCCESSFULLY (0 ERRORS)             ")
    print("==========================================================================")

if __name__ == "__main__":
    test_serialization()
