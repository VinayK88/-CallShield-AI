<div align="center">

# ☎️ CallShield AI

### Voice Scam & Spam Call Intelligence Platform

**Scam Detection · Transcript NLP · Behavioral ML · Anomaly Detection · Ensemble Risk · Campaign Intelligence · Intervention Policy**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Multi--Page%20Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Behavioral%20ML-EC6B23?style=flat-square)](https://xgboost.ai/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Isolation%20Forest-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Trust & Safety](https://img.shields.io/badge/Trust%20%26%20Safety-Voice%20Calls-238636?style=flat-square)](#)

**call → transcript intelligence → behavioral ML → novelty detection → ensemble score → campaign context → intervention**

</div>

---

## 📊 Dashboard preview

<p align="center"><img src="assets/dashboard-preview.svg" alt="CallShield AI dashboard preview" width="100%" /></p>

> Executive and analyst view of scam prevalence, model quality, spoofing, robotic-call activity, user protection, campaign risk, and intervention decisions.

---

## Product concept

CallShield AI is a portfolio-grade Trust & Safety data science platform for protecting a consumer calling ecosystem from **robocalls, telemarketing abuse, bank impersonation, tech-support scams, government impersonation, account-takeover scams, and investment scams**.

The project combines **transcript NLP, nonlinear caller-behavior modeling, acoustic-style indicators, spoofing signals, unsupervised novelty detection, ensemble risk scoring, campaign intelligence, proportional interventions, and operational KPI monitoring**. All data is synthetic.

## Scam taxonomy

`LEGITIMATE · ROBOCALL · TELEMARKETING · BANK IMPERSONATION · TECH SUPPORT SCAM · GOVERNMENT IMPERSONATION · ACCOUNT TAKEOVER SCAM · INVESTMENT / CRYPTO SCAM`

## Signal architecture

| Signal family | Examples |
|---|---|
| **Transcript** | urgency, credential requests, payment language, repeated scripts |
| **Behavioral** | calls/hour, unique recipients/hour, prior reports, duration |
| **Identity / spoofing** | new number, spoof indicator |
| **Acoustic proxy** | robotic-voice score |
| **Campaign** | fan-out, repetition, spoof rate, report concentration |

The baseline model selects an operating threshold to maximize scam recall while keeping false-positive rate near a strict **≤2% guardrail**.

---

## 🧠 ML Model Lab

CallShield now includes a dedicated advanced-modeling layer in `src/model_lab.py`.

```text
Behavioral features ──► XGBoost classifier ─────────┐
                                                     │
Legitimate baseline ─► Isolation Forest anomaly ────┼──► Ensemble Champion Score
                                                     │
                                                     ▼
                                        threshold under ≤2% FPR
                                                     │
                                                     ▼
                          ALLOW → LABEL → SCREEN → SILENCE → BLOCK
```

### Models

| Model | Purpose |
|---|---|
| **XGBoost Behavioral** | nonlinear interactions across velocity, fan-out, reports, spoofing, acoustic proxy, urgency, and recovery/payment cues |
| **Isolation Forest** | flag previously unseen behavior without requiring a known scam label |
| **Ensemble Champion** | combines supervised risk with novelty sensitivity |
| **Logistic + TF-IDF baseline** | transparent transcript + numeric benchmark |

If XGBoost is unavailable, the code automatically falls back to a balanced Random Forest so the lab remains runnable.

### Evaluation

Each model is evaluated on the same holdout sample using:

**PR-AUC · ROC-AUC · Precision · Recall · False-positive rate · Operating threshold**

Thresholds are selected under the same **≤2% false-positive guardrail**, making the comparison product-oriented rather than accuracy-only.

### Explainability

The ML Model Lab produces ranked tree feature importance across:

`recipient fan-out · call velocity · reports · spoof signal · repeated-script similarity · robotic-voice score · urgency · credential/payment requests · duration · number age`

A production extension can replace or augment this with per-call SHAP explanations.

---

## Intervention ladder

`ALLOW → LABEL SUSPECTED SPAM → CALL SCREEN → SILENCE → BLOCK`

Prediction and intervention are intentionally separated so model risk can be translated into proportional product policy.

## Executive KPIs

**Scam prevalence · Detection recall · Precision · False-positive rate · PR-AUC · High-risk traffic · Blocked calls · Call-screen rate · Spoof-signal rate · Robotic-call rate · Average recipient reach · Estimated users protected**

## Multi-page dashboard

1. `dashboard/app.py` — **Command Center**
2. `dashboard/pages/1_Scam_Intelligence.py` — **Scam Intelligence**
3. `dashboard/pages/2_Campaign_Intelligence.py` — **Campaign Intelligence**
4. `dashboard/pages/3_Intervention_Policy.py` — **Intervention Policy**
5. `dashboard/pages/4_ML_Model_Lab.py` — **ML Model Lab**

The **ML Model Lab** presents the champion model, PR-AUC/ROC-AUC, recall, precision, FPR, full model comparison, feature importance, and a per-call investigation surface showing **behavioral ML score vs anomaly score vs ensemble score**.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_pipeline.py --rows 30000
streamlit run dashboard/app.py
```

The pipeline writes:

```text
outputs/scored_calls.csv
outputs/campaigns.csv
outputs/ml_lab_scored.csv
outputs/model_comparison.csv
outputs/feature_importance.csv
outputs/ml_lab_summary.json
```

## Production evolution

A real system could add **multilingual ASR, transformer transcript embeddings, speaker embeddings, SHAP explanations, STIR/SHAKEN attestation, carrier reputation, device/number graph features, sequence models, temporal graph neural networks, calibrated market-specific thresholds, challenger-vs-champion monitoring, analyst feedback loops, and privacy-preserving aggregation**.

---

<div align="center">

### Protect people from harmful calls without disrupting legitimate communication.

**Voice Safety · NLP · XGBoost · Anomaly Detection · Ensemble ML · Campaign Detection · Policy Decisioning**

</div>
