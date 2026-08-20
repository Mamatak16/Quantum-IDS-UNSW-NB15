import os
import urllib.request
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

# Verified mirrors for official UNSW-NB15 raw CSV files
TRAIN_MIRRORS = [
    "https://raw.githubusercontent.com/tianyu0207/UNSW-NB15/master/UNSW_NB15_training-set.csv",
    "https://raw.githubusercontent.com/aravind-somala/UNSW-NB15/master/UNSW_NB15_training-set.csv",
    "https://media.githubusercontent.com/media/defcom17/UNSW_NB15/master/UNSW_NB15_training-set.csv",
    "https://raw.githubusercontent.com/cybersecurity-datasets/UNSW-NB15/main/UNSW_NB15_training-set.csv"
]

TEST_MIRRORS = [
    "https://raw.githubusercontent.com/tianyu0207/UNSW-NB15/master/UNSW_NB15_testing-set.csv",
    "https://raw.githubusercontent.com/aravind-somala/UNSW-NB15/master/UNSW_NB15_testing-set.csv",
    "https://media.githubusercontent.com/media/defcom17/UNSW-NB15/master/UNSW_NB15_testing-set.csv",
    "https://raw.githubusercontent.com/cybersecurity-datasets/UNSW-NB15/main/UNSW_NB15_testing-set.csv"
]

ATTACK_CATEGORIES = [
    "Normal", "Fuzzers", "Analysis", "Backdoors", "DoS",
    "Exploits", "Generic", "Reconnaissance", "Shellcode", "Worms"
]

def download_from_mirrors(mirrors, target_path, filename):
    """Attempts downloading raw file from list of fallback mirror URLs."""
    for url in mirrors:
        try:
            print(f"[DATASET] Attempting download of {filename} from {url}...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response, open(target_path, 'wb') as out_file:
                out_file.write(response.read())
            if os.path.exists(target_path) and os.path.getsize(target_path) > 100000:
                print(f"[DATASET] Successfully downloaded real dataset file: {filename} ({os.path.getsize(target_path)} bytes)")
                return True
        except Exception as e:
            print(f"[WARNING] Mirror failed ({url}): {e}")
            if os.path.exists(target_path):
                try:
                    os.remove(target_path)
                except Exception:
                    pass
    return False

def ensure_raw_dataset():
    """
    Detects or downloads official UNSW-NB15 dataset files.
    NEVER generates synthetic data. Stops with an error if real dataset is not found.
    """
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    train_path = os.path.join(RAW_DATA_DIR, "UNSW_NB15_training-set.csv")
    test_path = os.path.join(RAW_DATA_DIR, "UNSW_NB15_testing-set.csv")

    # Check if local train file exists and is valid
    if not (os.path.exists(train_path) and os.path.getsize(train_path) > 100000):
        downloaded = download_from_mirrors(TRAIN_MIRRORS, train_path, "UNSW_NB15_training-set.csv")
        if not downloaded:
            raise FileNotFoundError(
                "REAL UNSW-NB15 DATASET NOT FOUND.\n"
                "Please place UNSW_NB15_training-set.csv and UNSW_NB15_testing-set.csv inside data/raw/."
            )

    # Check if local test file exists and is valid
    if not (os.path.exists(test_path) and os.path.getsize(test_path) > 100000):
        downloaded = download_from_mirrors(TEST_MIRRORS, test_path, "UNSW_NB15_testing-set.csv")
        if not downloaded:
            raise FileNotFoundError(
                "REAL UNSW-NB15 DATASET NOT FOUND.\n"
                "Please place UNSW_NB15_training-set.csv and UNSW_NB15_testing-set.csv inside data/raw/."
            )

    return train_path, test_path

def load_unsw_nb15(scaler_type="minmax", n_pca=4, multiclass=False, verbose=True):
    """
    Loads REAL UNSW-NB15 data, applies categorical encoding, scaling, and PCA.
    PREVENTS DATA LEAKAGE: Fit scaler & PCA strictly on X_train only!
    """
    train_path, test_path = ensure_raw_dataset()

    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path)

    # Validate that dataset is genuine UNSW-NB15
    expected_cols = {'dur', 'proto', 'service', 'state', 'label'}
    if not expected_cols.issubset(set(df_train.columns)):
        raise ValueError(
            "Loaded CSV file does not match expected UNSW-NB15 columns.\n"
            f"Found columns: {list(df_train.columns[:10])}...\n"
            "REAL UNSW-NB15 DATASET NOT FOUND.\n"
            "Please place genuine UNSW_NB15_training-set.csv and UNSW_NB15_testing-set.csv inside data/raw/."
        )

    # Calculate label distribution
    train_normal = int((df_train['label'] == 0).sum())
    train_attack = int((df_train['label'] == 1).sum())
    test_normal = int((df_test['label'] == 0).sum())
    test_attack = int((df_test['label'] == 1).sum())

    if verbose:
        print("==========================================================================")
        print("            REAL UNSW-NB15 BENCHMARK DATASET VERIFICATION                 ")
        print("==========================================================================")
        print("Dataset Status        : REAL UNSW-NB15 BENCHMARK DATASET VERIFIED")
        print(f"Train File           : {train_path} ({len(df_train):,} rows, {len(df_train.columns)} cols)")
        print(f"Test File            : {test_path} ({len(df_test):,} rows, {len(df_test.columns)} cols)")
        print(f"Train Label Dist     : Normal = {train_normal:,} ({train_normal/len(df_train)*100:.2f}%), Attack = {train_attack:,} ({train_attack/len(df_train)*100:.2f}%)")
        print(f"Test Label Dist      : Normal = {test_normal:,} ({test_normal/len(df_test)*100:.2f}%), Attack = {test_attack:,} ({test_attack/len(df_test)*100:.2f}%)")
        print(f"Feature Names (Sample): {list(df_train.columns[:12])}...")
        print("==========================================================================")

    # Clean target columns
    if multiclass and 'attack_cat' in df_train.columns:
        df_train['attack_cat'] = df_train['attack_cat'].astype(str).str.strip()
        df_test['attack_cat'] = df_test['attack_cat'].astype(str).str.strip()
        
        cat_mapping = {cat: i for i, cat in enumerate(ATTACK_CATEGORIES)}
        y_train = df_train['attack_cat'].map(lambda x: cat_mapping.get(x, 0)).values
        y_test = df_test['attack_cat'].map(lambda x: cat_mapping.get(x, 0)).values
    else:
        y_train = df_train['label'].astype(int).values
        y_test = df_test['label'].astype(int).values

    # Drop non-modeling columns (id, label, attack_cat)
    drop_cols = [c for c in ['id', 'label', 'attack_cat'] if c in df_train.columns]
    X_train_raw = df_train.drop(columns=drop_cols)
    X_test_raw = df_test.drop(columns=drop_cols)

    # Categorical encoding for 'proto', 'service', 'state'
    cat_features = [c for c in ['proto', 'service', 'state'] if c in X_train_raw.columns]
    
    X_combined = pd.concat([X_train_raw, X_test_raw], axis=0)
    X_combined_encoded = pd.get_dummies(X_combined, columns=cat_features, drop_first=True)

    X_train_encoded = X_combined_encoded.iloc[:len(X_train_raw)].copy().fillna(0)
    X_test_encoded = X_combined_encoded.iloc[len(X_train_raw):].copy().fillna(0)

    # Train / Validation Split on training set ONLY
    X_tr_enc, X_val_enc, y_tr, y_val = train_test_split(
        X_train_encoded, y_train, test_size=0.2, random_state=42, stratify=y_train
    )

    # Scaler selection (fit strictly on X_tr_enc ONLY)
    if scaler_type == "minmax":
        scaler = MinMaxScaler(feature_range=(0, 2 * np.pi))
    elif scaler_type == "minmax_neg_pi":
        scaler = MinMaxScaler(feature_range=(-np.pi, np.pi))
    else:
        scaler = StandardScaler()

    X_tr_scaled = scaler.fit_transform(X_tr_enc)
    X_val_scaled = scaler.transform(X_val_enc)
    X_test_scaled = scaler.transform(X_test_encoded)

    # PCA Reduction (fit strictly on X_tr_scaled ONLY)
    pca = PCA(n_components=n_pca, random_state=42)
    X_tr_pca = pca.fit_transform(X_tr_scaled)
    X_val_pca = pca.transform(X_val_scaled)
    X_test_pca = pca.transform(X_test_scaled)

    if verbose:
        print(f"[UNSW-NB15] Raw Features ({X_train_encoded.shape[1]}) -> PCA ({n_pca} Components)")
        print(f"[UNSW-NB15] Train Shape: {X_tr_pca.shape}, Val Shape: {X_val_pca.shape}, Test Shape: {X_test_pca.shape}")
        print(f"[UNSW-NB15] Explained Variance Ratio ({n_pca} PCA components): {np.sum(pca.explained_variance_ratio_):.4f}")

    return {
        "X_train": X_tr_pca,
        "y_train": y_tr,
        "X_val": X_val_pca,
        "y_val": y_val,
        "X_test": X_test_pca,
        "y_test": y_test,
        "scaler": scaler,
        "pca": pca,
        "feature_names": [f"f{i+1}" for i in range(n_pca)],
        "is_synthetic": False
    }
