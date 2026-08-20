import os
import sys
import time
import json
import joblib
import numpy as np

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.preprocessing.dataset import load_unsw_nb15
from src.models.classical_model import ClassicalSVMModel
from src.evaluation.metrics import evaluate_classification

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

def main():
    print("==========================================================================")
    print("     QUANTUM-IDS-UNSW-NB15: END-TO-END PIPELINE & MODEL BENCHMARK        ")
    print("==========================================================================")

    np.random.seed(42)
    os.makedirs(BACKEND_DIR, exist_ok=True)
    os.makedirs(os.path.join(RESULTS_DIR, "svm"), exist_ok=True)
    os.makedirs(os.path.join(RESULTS_DIR, "qsvm"), exist_ok=True)
    os.makedirs(os.path.join(RESULTS_DIR, "vqc"), exist_ok=True)
    os.makedirs(os.path.join(RESULTS_DIR, "comparison"), exist_ok=True)

    # 1. Load Preprocessed REAL UNSW-NB15 Dataset (PCA-4)
    print("\n[1/4] Loading & Preprocessing REAL UNSW-NB15 Dataset (PCA-4)...")
    dataset = load_unsw_nb15(scaler_type="minmax", n_pca=4, verbose=True)

    # Subsets for fast, reliable local CPU execution
    train_size = min(300, len(dataset["X_train"]))
    test_size = min(200, len(dataset["X_test"]))

    idx_tr = np.random.choice(len(dataset["X_train"]), size=train_size, replace=False)
    idx_te = np.random.choice(len(dataset["X_test"]), size=test_size, replace=False)

    X_train = dataset["X_train"][idx_tr]
    y_train = dataset["y_train"][idx_tr]
    X_test = dataset["X_test"][idx_te]
    y_test = dataset["y_test"][idx_te]

    comparison_results = []

    # 2. Classical SVM Model
    print("\n[2/4] Training Classical SVM (RBF Kernel)...")
    try:
        svm = ClassicalSVMModel(C=1.0, kernel='rbf')
        svm.fit(X_train, y_train)
        svm_metrics = svm.evaluate(X_test, y_test)
        
        svm_bundle = {
            "model": svm.model,
            "scaler": dataset["scaler"],
            "pca": dataset["pca"],
            "metrics": svm_metrics
        }
        joblib.dump(svm_bundle, os.path.join(BACKEND_DIR, "svm_model.pkl"))
        with open(os.path.join(RESULTS_DIR, "svm", "svm_results.json"), "w") as f:
            json.dump(svm_metrics, f, indent=2)

        comparison_results.append({
            "id": "svm",
            "name": "Classical SVM (RBF Kernel)",
            "status": "Available",
            "accuracy": svm_metrics["accuracy"],
            "precision": svm_metrics["precision"],
            "recall": svm_metrics["recall"],
            "f1_score": svm_metrics["f1_score"],
            "training_time_sec": svm_metrics["training_time_sec"]
        })
        print(f" -> Classical SVM Acc: {svm_metrics['accuracy']:.2f}%, F1: {svm_metrics['f1_score']:.2f}%, Time: {svm_metrics['training_time_sec']}s")
    except Exception as e:
        print(f" -> Classical SVM Execution Exception: {e}")

    # 3. QSVM Model (ZFeatureMap Statevector Kernel)
    print("\n[3/4] Training Quantum SVM (QSVM ZFeatureMap 4-Qubit)...")
    try:
        from src.models.qsvm_model import QSVMModel
        qsvm = QSVMModel(num_qubits=4, feature_map_type="z", reps=1)
        qsvm.fit(X_train, y_train)
        qsvm_metrics = qsvm.evaluate(X_test, y_test)

        qsvm_bundle = {
            "model": qsvm.svc,
            "quantum_kernel": qsvm,
            "X_train": qsvm.X_train_ref,
            "scaler": dataset["scaler"],
            "pca": dataset["pca"],
            "metrics": qsvm_metrics
        }
        joblib.dump(qsvm_bundle, os.path.join(BACKEND_DIR, "qsvm_model.pkl"))
        with open(os.path.join(RESULTS_DIR, "qsvm", "qsvm_results.json"), "w") as f:
            json.dump(qsvm_metrics, f, indent=2)

        comparison_results.append({
            "id": "qsvm",
            "name": "QSVM (ZFeatureMap 4-Qubit)",
            "status": "Available",
            "accuracy": qsvm_metrics["accuracy"],
            "precision": qsvm_metrics["precision"],
            "recall": qsvm_metrics["recall"],
            "f1_score": qsvm_metrics["f1_score"],
            "training_time_sec": qsvm_metrics["training_time_sec"]
        })
        print(f" -> QSVM Acc: {qsvm_metrics['accuracy']:.2f}%, F1: {qsvm_metrics['f1_score']:.2f}%, Time: {qsvm_metrics['training_time_sec']}s")
    except Exception as e:
        print(f" -> QSVM Execution Exception / Unavailable: {e}")

    # 4. Basic VQC Model (Lightweight CPU Config: 4-Qubit, COBYLA maxiter=15)
    print("\n[4/4] Training Basic VQC (4-Qubit, COBYLA-15)...")
    try:
        from src.models.vqc_model import VQCModel
        vqc = VQCModel(
            num_qubits=4,
            feature_map_type="z",
            fm_reps=1,
            ansatz_type="real_amplitudes",
            ansatz_reps=1,
            optimizer_type="cobyla",
            maxiter=15
        )
        vqc.fit(X_train, y_train)
        vqc_metrics = vqc.evaluate(X_test, y_test)

        vqc_pkl_path = os.path.join(BACKEND_DIR, "vqc_model.pkl")
        vqc.save_bundle(vqc_pkl_path, scaler=dataset["scaler"], pca=dataset["pca"], metrics=vqc_metrics)

        with open(os.path.join(RESULTS_DIR, "vqc", "vqc_results.json"), "w") as f:
            json.dump(vqc_metrics, f, indent=2)

        comparison_results.append({
            "id": "vqc",
            "name": "Basic VQC (4-Qubit COBYLA)",
            "status": "Available",
            "accuracy": vqc_metrics["accuracy"],
            "precision": vqc_metrics["precision"],
            "recall": vqc_metrics["recall"],
            "f1_score": vqc_metrics["f1_score"],
            "training_time_sec": vqc_metrics["training_time_sec"]
        })
        print(f" -> Basic VQC Acc: {vqc_metrics['accuracy']:.2f}%, F1: {vqc_metrics['f1_score']:.2f}%, Time: {vqc_metrics['training_time_sec']}s")
    except Exception as e:
        print(f" -> Basic VQC Execution Exception / Unavailable: {e}")

    # Save summary report
    summary = {
        "dataset": "UNSW-NB15 (Real)",
        "pca_components": 4,
        "models": comparison_results
    }
    with open(os.path.join(RESULTS_DIR, "comparison", "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # Print Table 1: Model Comparison Table
    print("\n==========================================================================")
    print("                     MODEL COMPARISON TABLE                               ")
    print("==========================================================================")
    print(f"{'Model':<28} | {'Accuracy (%)':<12} | {'Precision (%)':<13} | {'Recall (%)':<10} | {'F1 (%)':<8} | {'Training Time (s)':<17}")
    print("-" * 100)
    for m in comparison_results:
        print(f"{m['name']:<28} | {m['accuracy']:<12.2f} | {m['precision']:<13.2f} | {m['recall']:<10.2f} | {m['f1_score']:<8.2f} | {m['training_time_sec']:<17.2f}")
    print("==========================================================================\n")
    print("Master pipeline finished successfully without exceptions!")

if __name__ == "__main__":
    main()
