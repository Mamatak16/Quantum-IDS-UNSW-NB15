import os
import sys
import json
import time
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing.dataset import load_unsw_nb15
from src.models.vqc_model import VQCModel
from src.models.classical_model import ClassicalSVMModel
from src.models.qsvm_model import QSVMModel
from src.evaluation.metrics import evaluate_classification

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results", "vqc")
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

def run_systematic_vqc_experiment():
    print("==========================================================================")
    print("   UNSW-NB15 SYSTEMATIC VQC HYPERPARAMETER EXPERIMENT FRAMEWORK          ")
    print("==========================================================================")

    np.random.seed(42)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(BACKEND_DIR, exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "results", "comparison"), exist_ok=True)

    # 1. Define systematic trial grid
    configs = [
        {
            "id": 1,
            "name": "Trial 1 (Baseline: StandardScaler + ZFeatureMap + RealAmplitudes-1 + COBYLA-30)",
            "n_pca": 4,
            "scaler": "standard",
            "feature_map_type": "z",
            "fm_reps": 1,
            "ansatz_type": "real_amplitudes",
            "ansatz_reps": 1,
            "entanglement": "linear",
            "optimizer_type": "cobyla",
            "maxiter": 30
        },
        {
            "id": 2,
            "name": "Trial 2 (MinMaxScaler 0..2pi + ZFeatureMap + RealAmplitudes-2 + COBYLA-40)",
            "n_pca": 4,
            "scaler": "minmax",
            "feature_map_type": "z",
            "fm_reps": 1,
            "ansatz_type": "real_amplitudes",
            "ansatz_reps": 2,
            "entanglement": "full",
            "optimizer_type": "cobyla",
            "maxiter": 40
        },
        {
            "id": 3,
            "name": "Trial 3 (MinMaxScaler + ZFeatureMap + EfficientSU2-2 + SPSA-40)",
            "n_pca": 4,
            "scaler": "minmax",
            "feature_map_type": "z",
            "fm_reps": 1,
            "ansatz_type": "efficient_su2",
            "ansatz_reps": 2,
            "entanglement": "full",
            "optimizer_type": "spsa",
            "maxiter": 40
        },
        {
            "id": 4,
            "name": "Trial 4 (MinMaxScaler + ZZFeatureMap-Full + EfficientSU2-2 + COBYLA-50)",
            "n_pca": 4,
            "scaler": "minmax",
            "feature_map_type": "zz_full",
            "fm_reps": 1,
            "ansatz_type": "efficient_su2",
            "ansatz_reps": 2,
            "entanglement": "full",
            "optimizer_type": "cobyla",
            "maxiter": 50
        },
        {
            "id": 5,
            "name": "Trial 5 (6-PCA Components + MinMaxScaler + EfficientSU2-2 + COBYLA-40)",
            "n_pca": 6,
            "scaler": "minmax",
            "feature_map_type": "z",
            "fm_reps": 1,
            "ansatz_type": "efficient_su2",
            "ansatz_reps": 2,
            "entanglement": "full",
            "optimizer_type": "cobyla",
            "maxiter": 40
        },
        {
            "id": 6,
            "name": "Trial 6 (6-PCA Components + ZZFeatureMap-Linear + RealAmplitudes-2 + SPSA-40)",
            "n_pca": 6,
            "scaler": "minmax",
            "feature_map_type": "zz_linear",
            "fm_reps": 1,
            "ansatz_type": "real_amplitudes",
            "ansatz_reps": 2,
            "entanglement": "full",
            "optimizer_type": "spsa",
            "maxiter": 40
        },
        {
            "id": 7,
            "name": "Trial 7 (8-PCA Components + MinMaxScaler + EfficientSU2-2 + COBYLA-40)",
            "n_pca": 8,
            "scaler": "minmax",
            "feature_map_type": "z",
            "fm_reps": 1,
            "ansatz_type": "efficient_su2",
            "ansatz_reps": 2,
            "entanglement": "full",
            "optimizer_type": "cobyla",
            "maxiter": 40
        }
    ]

    # Pre-cache preprocessed datasets for required (scaler, PCA) combinations
    data_cache = {}
    for sc in ["standard", "minmax"]:
        for p_dim in [4, 6, 8]:
            print(f"[PREPROCESSING] Cache setup: Scaler={sc}, PCA={p_dim}...")
            data_cache[(sc, p_dim)] = load_unsw_nb15(scaler_type=sc, n_pca=p_dim, verbose=False)

    # Controlled subsets for fast execution (250 train, 150 val, 300 test)
    std4_ref = data_cache[("standard", 4)]
    idx_tr = np.random.choice(len(std4_ref["X_train"]), size=250, replace=False)
    idx_val = np.random.choice(len(std4_ref["X_val"]), size=150, replace=False)
    idx_te = np.random.choice(len(std4_ref["X_test"]), size=300, replace=False)

    trials_summary = []
    best_val_acc = -1.0
    best_config = None
    best_vqc_model = None

    print("\n--------------------------------------------------------------------------")
    print("      PART 1: SYSTEMATIC VQC HYPERPARAMETER VALIDATION SEARCH            ")
    print("--------------------------------------------------------------------------")

    for cfg in configs:
        sc = cfg["scaler"]
        p_dim = cfg["n_pca"]
        data = data_cache[(sc, p_dim)]

        X_tr_sub = data["X_train"][idx_tr]
        y_tr_sub = data["y_train"][idx_tr]
        X_val_sub = data["X_val"][idx_val]
        y_val_sub = data["y_val"][idx_val]

        vqc = VQCModel(
            num_qubits=p_dim,
            feature_map_type=cfg["feature_map_type"],
            fm_reps=cfg["fm_reps"],
            ansatz_type=cfg["ansatz_type"],
            ansatz_reps=cfg["ansatz_reps"],
            entanglement=cfg.get("entanglement", "full"),
            optimizer_type=cfg["optimizer_type"],
            maxiter=cfg["maxiter"]
        )

        t_start = time.time()
        vqc.fit(X_tr_sub, y_tr_sub)
        t_sec = round(time.time() - t_start, 2)

        val_metrics = vqc.evaluate(X_val_sub, y_val_sub)
        val_acc = val_metrics["accuracy"]
        val_f1 = val_metrics["f1_score"]

        print(f"[{cfg['name']}] -> Val Acc: {val_acc:.2f}%, Val F1: {val_f1:.2f}%, Time: {t_sec}s")

        trials_summary.append({
            "trial_id": cfg["id"],
            "pca": p_dim,
            "scaler": sc,
            "feature_map": cfg["feature_map_type"],
            "ansatz": cfg["ansatz_type"],
            "optimizer": cfg["optimizer_type"],
            "iterations": cfg["maxiter"],
            "val_accuracy": val_acc,
            "val_precision": val_metrics["precision"],
            "val_recall": val_metrics["recall"],
            "val_f1": val_f1,
            "training_time_sec": t_sec,
            "config": cfg,
            "model_obj": vqc
        })

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_config = cfg
            best_vqc_model = vqc

    # Save trials table to CSV & JSON
    df_trials = pd.DataFrame([{
        "PCA": t["pca"],
        "Scaler": t["scaler"],
        "Feature Map": t["feature_map"],
        "Ansatz": t["ansatz"],
        "Optimizer": t["optimizer"],
        "Iterations": t["iterations"],
        "Validation Accuracy (%)": t["val_accuracy"],
        "Validation F1 (%)": t["val_f1"],
        "Training Time (s)": t["training_time_sec"]
    } for t in trials_summary])

    df_trials.to_csv(os.path.join(RESULTS_DIR, "vqc_trials.csv"), index=False)

    print("\n--------------------------------------------------------------------------")
    print("      PART 2: UNTOUCHED TEST SET EVALUATION (BEST VQC MODEL ONLY)         ")
    print("--------------------------------------------------------------------------")

    best_data = data_cache[(best_config["scaler"], best_config["n_pca"])]
    X_test_sub = best_data["X_test"][idx_te]
    y_test_sub = best_data["y_test"][idx_te]

    opt_test_metrics = best_vqc_model.evaluate(X_test_sub, y_test_sub)

    # Evaluate Baseline VQC on same test set for fair comparison
    baseline_vqc_model = trials_summary[0]["model_obj"]
    base_data = data_cache[(configs[0]["scaler"], configs[0]["n_pca"])]
    baseline_test_metrics = baseline_vqc_model.evaluate(base_data["X_test"][idx_te], y_test_sub)

    # 3. Train & Evaluate Classical SVM & QSVM baselines
    print("\n--------------------------------------------------------------------------")
    print("      PART 3: BASELINE MODELS COMPARISON (SVM & QSVM)                     ")
    print("--------------------------------------------------------------------------")

    svm_model = ClassicalSVMModel(C=1.0, kernel='rbf')
    svm_model.fit(std4_ref["X_train"][idx_tr], std4_ref["y_train"][idx_tr])
    svm_test_metrics = svm_model.evaluate(std4_ref["X_test"][idx_te], y_test_sub)

    qsvm_model = QSVMModel(num_qubits=4, feature_map_type="z", reps=1)
    qsvm_model.fit(std4_ref["X_train"][idx_tr], std4_ref["y_train"][idx_tr])
    qsvm_test_metrics = qsvm_model.evaluate(std4_ref["X_test"][idx_te], y_test_sub)

    # Save best VQC model bundle to backend using pickle-safe save_bundle
    vqc_pkl_path = os.path.join(BACKEND_DIR, "vqc_model.pkl")
    best_vqc_model.save_bundle(vqc_pkl_path, scaler=best_data["scaler"], pca=best_data["pca"], metrics=opt_test_metrics)

    # Save all results to JSON
    exp_report = {
        "dataset": "UNSW-NB15 (Real)",
        "best_config": best_config,
        "vqc_baseline_test": baseline_test_metrics,
        "vqc_optimized_test": opt_test_metrics,
        "improvement_pct_points": round(opt_test_metrics["accuracy"] - baseline_test_metrics["accuracy"], 2),
        "svm_test": svm_test_metrics,
        "qsvm_test": qsvm_test_metrics,
        "trials": [{k: v for k, v in t.items() if k != "model_obj"} for t in trials_summary]
    }

    with open(os.path.join(RESULTS_DIR, "vqc_experiment_results.json"), "w") as f:
        json.dump(exp_report, f, indent=2)

    # Print Table 1: Model Comparison Table
    print("\n==========================================================================")
    print("                   TABLE 1: FAIR MODEL COMPARISON                         ")
    print("==========================================================================")
    print(f"{'Model':<20} | {'Accuracy (%)':<12} | {'Precision (%)':<13} | {'Recall (%)':<10} | {'F1 (%)':<8} | {'Training Time (s)':<17}")
    print("-" * 92)
    models_list = [
        ("Classical SVM", svm_test_metrics),
        ("QSVM (ZFeatureMap)", qsvm_test_metrics),
        ("Baseline VQC", baseline_test_metrics),
        ("Optimized VQC", opt_test_metrics)
    ]
    for name, m in models_list:
        print(f"{name:<20} | {m['accuracy']:<12.2f} | {m['precision']:<13.2f} | {m['recall']:<10.2f} | {m['f1_score']:<8.2f} | {m['training_time_sec']:<17.2f}")
    print("==========================================================================\n")

    # Print Table 2: VQC Hyperparameter Optimization Grid Table
    print("==================================================================================================================")
    print("                    TABLE 2: VQC HYPERPARAMETER SEARCH TRIALS (VALIDATION SET)                             ")
    print("==================================================================================================================")
    print(f"{'PCA':<4} | {'Scaler':<12} | {'Feature Map':<16} | {'Ansatz':<16} | {'Optimizer':<10} | {'Iter':<5} | {'Val Acc (%)':<11} | {'Val F1 (%)':<10}")
    print("-" * 114)
    for t in trials_summary:
        print(f"{t['pca']:<4} | {t['scaler']:<12} | {t['feature_map']:<16} | {t['ansatz']:<16} | {t['optimizer']:<10} | {t['iterations']:<5} | {t['val_accuracy']:<11.2f} | {t['val_f1']:<10.2f}")
    print("==================================================================================================================\n")

    print(f"Winning VQC Config: {best_config['name']}")
    print(f"Baseline VQC Test Accuracy : {baseline_test_metrics['accuracy']:.2f}%")
    print(f"Optimized VQC Test Accuracy: {opt_test_metrics['accuracy']:.2f}%")
    print(f"VQC Improvement           : +{exp_report['improvement_pct_points']:.2f} percentage points\n")

if __name__ == "__main__":
    run_systematic_vqc_experiment()
