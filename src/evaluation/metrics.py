import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)

def evaluate_classification(y_true, y_pred, is_multiclass=False):
    """
    Computes comprehensive metrics: Accuracy, Precision, Recall, F1, Macro F1, and Confusion Matrix.
    """
    acc = accuracy_score(y_true, y_pred)
    
    if is_multiclass:
        prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        macro_f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
    else:
        prec = precision_score(y_true, y_pred, zero_division=0)
        rec = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        macro_f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)

    cm = confusion_matrix(y_true, y_pred).tolist()

    return {
        "accuracy": round(float(acc) * 100, 2),
        "precision": round(float(prec) * 100, 2),
        "recall": round(float(rec) * 100, 2),
        "f1_score": round(float(f1) * 100, 2),
        "macro_f1": round(float(macro_f1) * 100, 2),
        "confusion_matrix": cm
    }
