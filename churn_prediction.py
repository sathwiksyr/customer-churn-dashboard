# model.py  —  Train, compare & save all models
# Run once: python model.py
# This will create model/churn_model.pkl, model/encoders.pkl, model/metrics.pkl
 
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble         import RandomForestClassifier
from sklearn.linear_model     import LogisticRegression
from sklearn.svm              import SVC
from sklearn.preprocessing    import LabelEncoder
from sklearn.model_selection  import train_test_split
from sklearn.metrics          import (accuracy_score, precision_score,
                                      recall_score, f1_score, roc_auc_score)
try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False
 
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "Churn.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)
 
 
# ── Load & preprocess ─────────────────────────
def load_and_preprocess():
    df = pd.read_csv(DATA_PATH)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)
    df.drop(columns=["customerID"], inplace=True, errors="ignore")
 
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    cat_cols = [c for c in cat_cols if c != "Churn"]
 
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
 
    df["Churn"] = (df["Churn"] == "Yes").astype(int)
    return df, encoders
 
 
# ── Train & evaluate all models ───────────────
def train_all():
    df, encoders = load_and_preprocess()
    X = df.drop(columns=["Churn"])
    y = df["Churn"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
 
    models = {
        "Random Forest":      RandomForestClassifier(n_estimators=100, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "SVM":                SVC(probability=True, random_state=42),
    }
    if HAS_XGB:
        models["XGBoost"] = XGBClassifier(use_label_encoder=False,
                                          eval_metric="logloss", random_state=42)
 
    metrics  = {}
    best_f1  = 0
    best_model = None
    best_name  = ""
 
    for name, clf in models.items():
        print(f"Training {name}...")
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1]
 
        m = {
            "Accuracy":  round(accuracy_score(y_test, y_pred)  * 100, 2),
            "Precision": round(precision_score(y_test, y_pred) * 100, 2),
            "Recall":    round(recall_score(y_test, y_pred)    * 100, 2),
            "F1 Score":  round(f1_score(y_test, y_pred)        * 100, 2),
            "ROC AUC":   round(roc_auc_score(y_test, y_prob)   * 100, 2),
        }
        metrics[name] = m
        print(f"  {name}: Accuracy={m['Accuracy']}%  F1={m['F1 Score']}%")
 
        if m["F1 Score"] > best_f1:
            best_f1    = m["F1 Score"]
            best_model = clf
            best_name  = name
 
    print(f"\n✅ Best model: {best_name} (F1={best_f1}%)")
 
    # Save best model
    pickle.dump(best_model, open(os.path.join(MODEL_DIR, "churn_model.pkl"), "wb"))
    pickle.dump(encoders,   open(os.path.join(MODEL_DIR, "encoders.pkl"),    "wb"))
    pickle.dump(metrics,    open(os.path.join(MODEL_DIR, "metrics.pkl"),     "wb"))
    pickle.dump(best_name,  open(os.path.join(MODEL_DIR, "best_name.pkl"),   "wb"))
    pickle.dump(X.columns.tolist(), open(os.path.join(MODEL_DIR, "feature_names.pkl"), "wb"))
 
    print("✅ Saved: churn_model.pkl, encoders.pkl, metrics.pkl, best_name.pkl")
    return best_model, encoders, metrics, best_name
 
 
if __name__ == "__main__":
    train_all()
