import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.preprocessing.dataset import load_unsw_nb15, RAW_DATA_DIR

def main():
    print("\n--- UNSW-NB15 DATASET PREPROCESSING VERIFICATION ---")
    train_csv = os.path.join(RAW_DATA_DIR, "UNSW_NB15_training-set.csv")
    test_csv = os.path.join(RAW_DATA_DIR, "UNSW_NB15_testing-set.csv")

    try:
        data = load_unsw_nb15(scaler_type="minmax", n_pca=4, verbose=True)

        print("\n--- SUMMARY PREPROCESSING METRICS ---")
        print(f"X_train PCA Shape: {data['X_train'].shape}")
        print(f"y_train Shape    : {data['y_train'].shape}")
        print(f"X_val PCA Shape  : {data['X_val'].shape}")
        print(f"y_val Shape      : {data['y_val'].shape}")
        print(f"X_test PCA Shape : {data['X_test'].shape}")
        print(f"y_test Shape     : {data['y_test'].shape}")
        print(f"Synthetic Check  : {data['is_synthetic']} (False = Genuine Real Dataset)")

    except FileNotFoundError as fnf:
        print("\n" + "="*70)
        print("ERROR:", fnf)
        print("="*70)

if __name__ == "__main__":
    main()
