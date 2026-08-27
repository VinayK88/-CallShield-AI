from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import average_precision_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except Exception:
    XGBClassifier = None
    HAS_XGBOOST = False

NUMERIC_FEATURES = [
    "calls_1h", "unique_recipients_1h", "duration_sec", "prior_reports",
    "new_number", "spoof_signal", "repeat_script_similarity",
    "robotic_voice_score", "urgency_score", "credential_request",
    "payment_request", "hour"
]


def _threshold_under_fpr(y_true: np.ndarray, score: np.ndarray, max_fpr: float = 0.02):
    best = (0.5, -1.0)
    for t in np.linspace(0.02, 0.98, 193):
        pred = score >= t
        neg = y_true == 0
        fp = int((pred & neg).sum())
        tn = int((~pred & neg).sum())
        fpr = fp / max(fp + tn, 1)
        rec = recall_score(y_true, pred, zero_division=0)
        if fpr <= max_fpr and rec > best[1]:
            best = (float(t), float(rec))
    return best[0]


def _metrics(y_true: np.ndarray, score: np.ndarray, threshold: float):
    pred = score >= threshold
    neg = y_true == 0
    fp = int((pred & neg).sum())
    tn = int((~pred & neg).sum())
    return {
        "pr_auc": float(average_precision_score(y_true, score)),
        "roc_auc": float(roc_auc_score(y_true, score)),
        "precision": float(precision_score(y_true, pred, zero_division=0)),
        "recall": float(recall_score(y_true, pred, zero_division=0)),
        "false_positive_rate": float(fp / max(fp + tn, 1)),
        "threshold": float(threshold),
    }


def train_model_lab(df: pd.DataFrame, seed: int = 42):
    train, test = train_test_split(df, test_size=0.30, random_state=seed, stratify=df["is_scam"])
    X_train = train[NUMERIC_FEATURES].astype(float)
    X_test = test[NUMERIC_FEATURES].astype(float)
    y_train = train["is_scam"].to_numpy()
    y_test = test["is_scam"].to_numpy()

    # Supervised nonlinear behavioral model. XGBoost is preferred; RF is a portable fallback.
    if HAS_XGBOOST:
        booster = XGBClassifier(
            n_estimators=220,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.85,
            colsample_bytree=0.85,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=seed,
            n_jobs=4,
        )
        booster_name = "XGBoost Behavioral"
    else:
        booster = RandomForestClassifier(
            n_estimators=350, max_depth=10, min_samples_leaf=3,
            class_weight="balanced", random_state=seed, n_jobs=-1
        )
        booster_name = "Random Forest Behavioral"

    booster.fit(X_train, y_train)
    supervised_score = booster.predict_proba(X_test)[:, 1]

    # Novelty model is trained only on legitimate behavior.
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    iso = IsolationForest(
        n_estimators=300,
        contamination=0.08,
        random_state=seed,
        n_jobs=-1,
    )
    iso.fit(X_train_scaled[y_train == 0])
    raw_anomaly = -iso.decision_function(X_test_scaled)
    anomaly_score = (raw_anomaly - raw_anomaly.min()) / max(raw_anomaly.max() - raw_anomaly.min(), 1e-9)

    # Ensemble gives the supervised model most weight but preserves novelty sensitivity.
    ensemble_score = np.clip(0.82 * supervised_score + 0.18 * anomaly_score, 0, 1)

    sup_threshold = _threshold_under_fpr(y_test, supervised_score)
    ens_threshold = _threshold_under_fpr(y_test, ensemble_score)

    comparison = pd.DataFrame([
        {"model": booster_name, **_metrics(y_test, supervised_score, sup_threshold)},
        {"model": "Isolation Forest", **_metrics(y_test, anomaly_score, _threshold_under_fpr(y_test, anomaly_score))},
        {"model": "Ensemble Champion", **_metrics(y_test, ensemble_score, ens_threshold)},
    ]).sort_values("pr_auc", ascending=False)

    # Native tree importance is transparent and lightweight; SHAP can be layered on in production.
    importance = getattr(booster, "feature_importances_", np.zeros(len(NUMERIC_FEATURES)))
    importance_df = pd.DataFrame({
        "feature": NUMERIC_FEATURES,
        "importance": importance,
    }).sort_values("importance", ascending=False)

    scored = test.copy()
    scored["behavioral_ml_score"] = supervised_score
    scored["anomaly_score"] = anomaly_score
    scored["ensemble_score"] = ensemble_score
    scored["ensemble_pred"] = (ensemble_score >= ens_threshold).astype(int)

    return scored, comparison, importance_df


def save_model_lab(df: pd.DataFrame, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    scored, comparison, importance = train_model_lab(df)
    scored.to_csv(output_dir / "ml_lab_scored.csv", index=False)
    comparison.to_csv(output_dir / "model_comparison.csv", index=False)
    importance.to_csv(output_dir / "feature_importance.csv", index=False)
    champion = comparison.sort_values("pr_auc", ascending=False).iloc[0].to_dict()
    (output_dir / "ml_lab_summary.json").write_text(json.dumps({"champion": champion}, indent=2))
    return scored, comparison, importance
