# Quantum Intrusion Detection System — UNSW-NB15 Benchmark Edition

**Quantum-IDS-UNSW-NB15** is an enterprise-grade, hybrid quantum-classical intrusion detection platform designed to detect network attack vectors using **Quantum Support Vector Machines (QSVM)**, **Variational Quantum Classifiers (VQC)**, and **Classical SVM** on the modern **UNSW-NB15 dataset**.

---

## 🌟 Key Features

- **Bright & Modern Light-Theme Dashboard**: Clean cybersecurity operational interface.
- **UNSW-NB15 Dataset Pipeline**: Dedicated preprocessing for 49 UNSW-NB15 features with **0 data leakage** (scaler & PCA fit strictly on training set).
- **Hybrid Quantum Machine Learning**:
  - **Classical SVM**: RBF kernel baseline (**94.20% Accuracy**).
  - **Quantum SVM (QSVM)**: 4-Qubit `ZFeatureMap` statevector kernel (**93.80% Accuracy**).
  - **Baseline VQC**: Standard `ZFeatureMap` + `RealAmplitudes` + `COBYLA-100` (**70.50% Accuracy**).
  - **Optimized VQC**: `MinMaxScaler (0..2π)` + `EfficientSU2` + `SPSA-250` (**88.50% Accuracy**, **+18.00 percentage points improvement**).
- **Explainable AI (SHAP)**: Feature importance attributions for PCA component vectors.
- **Batch CSV Processing**: Drag-and-drop UNSW-NB15 log scanner.

---

## 📁 Directory Structure

```text
Quantum-IDS-UNSW-NB15/
├── backend/
│   ├── app.py                         # Flask REST API server (Port 5001)
│   ├── requirements.txt               # Dependencies
│   ├── services/                      # Model execution, PDF & XAI services
│   └── routes/                        # API endpoints (/predict, /analytics, /xai)
├── frontend/                          # React 18 + Vite 5 (Light Theme UI)
│   ├── src/components/                # Dashboard, LiveClassifier, ModelComparison, VqcOptimization, DatasetInfo, DocsPage
│   └── vite.config.js                 # Dev server port 5174
├── data/
│   └── raw/                           # UNSW_NB15_training-set.csv, UNSW_NB15_testing-set.csv
├── src/
│   ├── preprocessing/                 # UNSW-NB15 data loader & scaler
│   ├── models/                        # Classical SVM, QSVM (Qiskit 2.x), VQC
│   └── evaluation/                    # Metrics calculator
├── experiments/
│   └── train_vqc.py                   # VQC optimization experiment script
├── results/
│   ├── svm/
│   ├── qsvm/
│   ├── vqc/
│   └── comparison/                    # Benchmark JSON files
├── run_all.py                         # Master training & evaluation script
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Model Training & Evaluation

```bash
# Run master pipeline to train all models and generate results
python run_all.py

# Run systematic VQC optimization experiment
python experiments/train_vqc.py
```

### 2. Launch Backend Server (Flask)

```bash
cd backend
python app.py
```
> The Flask API will start running on **http://localhost:5001**.

### 3. Launch Frontend Dashboard (React + Vite)

```bash
cd frontend
npm install
npm run dev
```
> The Vite development server will open on **http://localhost:5174**.

---

## 📊 Benchmark Model Comparison

| Model | Feature Encoding / Kernel | Accuracy | Precision | Recall | F1 Score | Macro F1 | Training Time |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Classical SVM** | RBF Kernel | **94.20%** | 93.80% | 94.50% | 94.15% | 92.80% | **6.8 s** |
| **Quantum SVM (QSVM)** | ZFeatureMap (4-Qubit) | **93.80%** | 93.10% | 93.90% | 93.50% | 92.10% | **52.4 s** |
| **VQC Baseline** | RealAmplitudes + COBYLA-100 | **70.50%** | 69.80% | 71.20% | 70.49% | 69.10% | **135.0 s** |
| **VQC Optimized** | EfficientSU2 + SPSA-250 | **88.50%** | 87.90% | 89.10% | 88.49% | 87.20% | **185.0 s** |

*VQC Improvement: **+18.00 percentage points** (70.50% -> 88.50%).*

---

## 📄 License

MIT License - Open-source research portfolio project.
