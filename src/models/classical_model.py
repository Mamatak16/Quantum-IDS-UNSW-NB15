import time
import joblib
from sklearn.svm import SVC
from src.evaluation.metrics import evaluate_classification

class ClassicalSVMModel:
    def __init__(self, C=1.0, kernel='rbf', gamma='scale', probability=True):
        self.C = C
        self.kernel = kernel
        self.gamma = gamma
        self.probability = probability
        self.model = SVC(C=C, kernel=kernel, gamma=gamma, probability=probability, random_state=42)
        self.training_time_sec = 0.0

    def fit(self, X_train, y_train):
        start = time.time()
        self.model.fit(X_train, y_train)
        self.training_time_sec = round(time.time() - start, 2)
        return self

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X)
        return None

    def evaluate(self, X_test, y_test):
        start = time.time()
        y_pred = self.predict(X_test)
        pred_time = round((time.time() - start) / max(len(X_test), 1) * 1000, 3)
        metrics = evaluate_classification(y_test, y_pred)
        metrics["training_time_sec"] = self.training_time_sec
        metrics["prediction_time_ms"] = pred_time
        return metrics

    def save(self, filepath):
        joblib.dump(self.model, filepath)
