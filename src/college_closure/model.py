"""Temporal models: logistic baseline + XGBoost, recall@K, SHAP."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from college_closure.config import Settings
from college_closure.features import MODEL_FEATURE_COLUMNS

LOGGER = logging.getLogger(__name__)


def recall_at_k(y_true: np.ndarray, scores: np.ndarray, k: int) -> float:
    y_true = np.asarray(y_true)
    scores = np.asarray(scores)
    n = len(y_true)
    if n == 0 or k <= 0:
        return float("nan")
    k = min(int(k), n)
    order = np.argsort(-scores)[:k]
    denom = max(float(y_true.sum()), 1.0)
    return float(y_true[order].sum() / denom)


def available_features(df: pd.DataFrame) -> list[str]:
    return [c for c in MODEL_FEATURE_COLUMNS if c in df.columns]


def _xy(df: pd.DataFrame, features: list[str], label: str) -> tuple[pd.DataFrame, np.ndarray]:
    X = df[features].copy()
    for c in X.columns:
        X[c] = pd.to_numeric(X[c], errors="coerce")
    y = pd.to_numeric(df[label], errors="coerce").fillna(0).astype(int).to_numpy()
    return X, y


def _eval_block(y: np.ndarray, scores: np.ndarray, ks: list[int]) -> dict:
    out: dict = {"n": int(len(y)), "positives": int(y.sum()) if len(y) else 0}
    if len(y) == 0 or y.sum() == 0:
        out["pr_auc"] = float("nan")
        out["roc_auc"] = float("nan")
        for k in ks:
            out[f"recall_at_{k}"] = float("nan")
        return out
    out["pr_auc"] = float(average_precision_score(y, scores))
    try:
        out["roc_auc"] = float(roc_auc_score(y, scores))
    except ValueError:
        out["roc_auc"] = float("nan")
    for k in ks:
        out[f"recall_at_{k}"] = recall_at_k(y, scores, k)
    return out


def naive_scores(df: pd.DataFrame) -> dict[str, np.ndarray]:
    comp = pd.to_numeric(df["composite_score"], errors="coerce") if "composite_score" in df.columns else pd.Series(np.nan, index=df.index)
    naive_comp = (comp < 1.0).fillna(False).astype(float).to_numpy()
    if "enr_decline_5y_gt30" in df.columns:
        naive_enr = pd.to_numeric(df["enr_decline_5y_gt30"], errors="coerce").fillna(0).to_numpy()
    else:
        naive_enr = np.zeros(len(df))
    return {"composite_lt_1": naive_comp, "enr_decline_5y_gt30": naive_enr}


def _fit_logit(X: pd.DataFrame, y: np.ndarray) -> Pipeline:
    pipe = Pipeline(
        [
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
            (
                "clf",
                LogisticRegression(
                    max_iter=400,
                    class_weight="balanced",
                    solver="lbfgs",
                ),
            ),
        ]
    )
    pipe.fit(X, y)
    return pipe


def _fit_booster(X: pd.DataFrame, y: np.ndarray):
    pos = int(y.sum())
    neg = int(len(y) - pos)
    spw = (neg / pos) if pos else 1.0
    Xf = X.astype(float)
    try:
        import xgboost as xgb

        model = xgb.XGBClassifier(
            n_estimators=250,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.8,
            min_child_weight=5,
            scale_pos_weight=spw,
            eval_metric="aucpr",
            n_jobs=4,
            random_state=42,
        )
        model.fit(Xf, y)
        return model, "xgboost"
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("XGBoost unavailable (%s); using HistGradientBoosting", exc)
        from sklearn.ensemble import HistGradientBoostingClassifier

        model = HistGradientBoostingClassifier(
            max_depth=4,
            learning_rate=0.05,
            max_iter=200,
            class_weight="balanced",
            random_state=42,
        )
        model.fit(Xf, y)
        return model, "hist_gbm"


def predict_proba(model, X: pd.DataFrame) -> np.ndarray:
    Xf = X.astype(float)
    if hasattr(model, "predict_proba"):
        return model.predict_proba(Xf)[:, 1]
    return np.asarray(model.predict(Xf), dtype=float)


def shap_top(model, X: pd.DataFrame, features: list[str], n: int = 15) -> list[dict]:
    try:
        import shap
    except ImportError:
        LOGGER.warning("shap not installed; using feature_importances_ if present")
        if hasattr(model, "feature_importances_"):
            imp = np.asarray(model.feature_importances_, dtype=float)
            order = np.argsort(-imp)[:n]
            return [{"feature": features[i], "mean_abs_shap": float(imp[i])} for i in order]
        return []

    Xf = X.astype(float)
    med = Xf.median(numeric_only=True)
    Xf = Xf.fillna(med)
    sample = Xf.sample(n=min(800, len(Xf)), random_state=42) if len(Xf) > 800 else Xf
    try:
        explainer = shap.TreeExplainer(model)
        sv = explainer.shap_values(sample)
        if isinstance(sv, list):
            sv = sv[1]
        mean_abs = np.abs(np.asarray(sv)).mean(axis=0)
        order = np.argsort(-mean_abs)[:n]
        return [{"feature": features[i], "mean_abs_shap": float(mean_abs[i])} for i in order]
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("SHAP TreeExplainer failed (%s); using importances", exc)
        if hasattr(model, "feature_importances_"):
            imp = np.asarray(model.feature_importances_, dtype=float)
            order = np.argsort(-imp)[:n]
            return [{"feature": features[i], "mean_abs_shap": float(imp[i])} for i in order]
        return []


def _load_modeling_frame(settings: Settings) -> pd.DataFrame:
    processed = settings.processed_dir
    labels_path = processed / "labels.parquet"
    feat_path = processed / "features.parquet"
    if labels_path.exists():
        frame = pd.read_parquet(labels_path)
        if "closed_or_merged_within_3_years" in frame.columns:
            return frame
    if not feat_path.exists():
        raise FileNotFoundError("features.parquet / labels.parquet missing — run 04 and 05")
    feat = pd.read_parquet(feat_path)
    if "closed_or_merged_within_3_years" not in feat.columns and labels_path.exists():
        lab = pd.read_parquet(labels_path)
        lab_cols = [c for c in lab.columns if c.startswith("closed_or_merged") or c.startswith("label_complete") or c in {"event_year", "event_type", "event_source"}]
        feat = feat.merge(lab[["unitid", "year", *lab_cols]], on=["unitid", "year"], how="left")
    return feat


def run_model(settings: Settings) -> dict:
    feat = _load_modeling_frame(settings)
    label = "closed_or_merged_within_3_years"
    if label not in feat.columns:
        raise FileNotFoundError("labels not attached — run scripts/05_labels.py")

    if "in_risk_model_universe" in feat.columns:
        univ = feat.loc[feat["in_risk_model_universe"] == True].copy()  # noqa: E712
    else:
        univ = feat.loc[pd.to_numeric(feat.get("inst_control"), errors="coerce").isin([2, 3])].copy()

    if "label_complete_h3" in univ.columns:
        complete = univ.loc[univ["label_complete_h3"] == True].copy()  # noqa: E712
    else:
        complete = univ.loc[univ[label].notna()].copy()

    features = available_features(complete)
    LOGGER.info("Modeling on %s complete risk-universe rows; %s features", f"{len(complete):,}", len(features))

    cfg_model = settings.raw.get("model") or {}
    train_end = int(cfg_model.get("train_end", 2016))
    val_years = [int(y) for y in cfg_model.get("val_years", [2017, 2018, 2019])]
    test_years = [int(y) for y in cfg_model.get("test_years", [2020, 2021])]
    years_ok = set(pd.to_numeric(complete["year"], errors="coerce").dropna().astype(int))
    val_years = [y for y in val_years if y in years_ok]
    test_years = [y for y in test_years if y in years_ok]
    if not test_years:
        ymax = int(complete["year"].max())
        test_years = [ymax]
        val_years = [y for y in range(ymax - 3, ymax) if y in years_ok]
        train_end = min(train_end, ymax - 4)
        LOGGER.warning("Adjusted splits to train_end=%s val=%s test=%s", train_end, val_years, test_years)

    train = complete.loc[complete["year"] <= train_end]
    val = complete.loc[complete["year"].isin(val_years)]
    test = complete.loc[complete["year"].isin(test_years)]
    LOGGER.info("Split sizes train=%s val=%s test=%s", len(train), len(val), len(test))

    X_train, y_train = _xy(train, features, label)
    if y_train.sum() < 5:
        LOGGER.warning("Very few training positives (%s) — model will be weak", int(y_train.sum()))

    logit = _fit_logit(X_train, y_train)
    booster, booster_name = _fit_booster(X_train, y_train)

    ks = [int(k) for k in cfg_model.get("recall_at_k", [25, 50, 100])]
    metrics: dict = {
        "booster": booster_name,
        "features": features,
        "n_features": len(features),
        "splits": {
            "train_end": train_end,
            "val_years": val_years,
            "test_years": test_years,
            "train_n": int(len(train)),
            "train_pos": int(y_train.sum()),
            "val_n": int(len(val)),
            "test_n": int(len(test)),
        },
        "beats_naive": {},
    }

    for name, frame in (("train", train), ("val", val), ("test", test)):
        if frame.empty:
            metrics[name] = {}
            continue
        X, y = _xy(frame, features, label)
        logit_s = logit.predict_proba(X)[:, 1]
        boost_s = predict_proba(booster, X)
        block = {
            "logit": _eval_block(y, logit_s, ks),
            booster_name: _eval_block(y, boost_s, ks),
        }
        if name == "test":
            naive = naive_scores(frame)
            for nk, ns in naive.items():
                block[f"naive_{nk}"] = _eval_block(y, ns, ks)
            beats = False
            details = []
            for yr in test_years:
                sub = frame.loc[frame["year"] == yr]
                if sub.empty or int(sub[label].sum()) == 0:
                    details.append({"year": int(yr), "note": "no positives or empty"})
                    continue
                Xs, ys = _xy(sub, features, label)
                ms = predict_proba(booster, Xs)
                m_pr = float(average_precision_score(ys, ms)) if ys.sum() else float("nan")
                m_r50 = recall_at_k(ys, ms, 50)
                year_beat = False
                for nk, ns in naive_scores(sub).items():
                    n_pr = float(average_precision_score(ys, ns)) if ys.sum() else float("nan")
                    n_r50 = recall_at_k(ys, ns, 50)
                    better = (m_pr > n_pr + 1e-9) or (m_r50 > n_r50 + 1e-9)
                    year_beat = year_beat or better
                    details.append(
                        {
                            "year": int(yr),
                            "model_pr_auc": m_pr,
                            "model_recall_at_50": float(m_r50),
                            "baseline": nk,
                            "baseline_pr_auc": n_pr,
                            "baseline_recall_at_50": float(n_r50),
                            "beats": better,
                        }
                    )
                beats = beats or year_beat
            metrics["beats_naive"] = {"any_test_year": beats, "by_year": details}
        metrics[name] = block

    metrics["shap_global"] = shap_top(booster, X_train, features)

    score_frame = univ.copy()
    Xs, _ = _xy(score_frame, features, label)
    score_frame["risk_score"] = predict_proba(booster, Xs)
    score_frame["risk_score_logit"] = logit.predict_proba(Xs)[:, 1]
    dest = settings.processed_dir / "scored.parquet"
    score_frame.to_parquet(dest, index=False)
    metrics_path = settings.processed_dir / "model_metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    # Small committed-friendly copy of metrics (no row-level scores)
    settings.outputs_dir.mkdir(parents=True, exist_ok=True)
    (settings.outputs_dir / "model_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    LOGGER.info("Wrote %s and %s (%s rows)", metrics_path, dest, f"{len(score_frame):,}")
    return metrics
