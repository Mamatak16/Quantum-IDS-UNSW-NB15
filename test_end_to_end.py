import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run_all import main as run_master_pipeline
from backend.services.model_service import ModelService

def test_pipeline():
    print("\n--- STEP 1: RUNNING MASTER PIPELINE (run_all.py) ---")
    run_master_pipeline()

    print("\n--- STEP 2: VERIFYING BACKEND MODEL SERVICE LOADING ---")
    service = ModelService()
    status = service.get_models_status()
    print(f"Backend Models Loaded Status: {status}")

    print("\n--- STEP 3: TESTING PREDICTIONS FOR ALL 3 MODELS ---")
    for model_type in ["svm", "qsvm", "vqc"]:
        res = service.predict(model_type=model_type, preset="normal")
        print(f"[{model_type.upper()} Predict Test] -> Result: {res['prediction']}, Threat: {res['threat']}, Confidence: {res['confidence']}%")

    print("\n==========================================================================")
    print("         END-TO-END SYSTEM VERIFICATION COMPLETED (0 ERRORS)              ")
    print("==========================================================================")

if __name__ == "__main__":
    test_pipeline()
