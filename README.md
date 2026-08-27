<div align="center">

# ☎️ CallShield AI

### Voice Trust & Safety Intelligence

**Scam Detection · Transcript NLP · Behavioral ML · Anomaly Detection · Ensemble Risk · Campaign Intelligence · Intervention Policy**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Product%20Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Behavioral%20ML-EC6B23?style=flat-square)](https://xgboost.ai/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Isolation%20Forest-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Trust & Safety](https://img.shields.io/badge/Trust%20%26%20Safety-Voice%20Calls-238636?style=flat-square)](#)

**call → transcript intelligence → behavioral ML → novelty detection → ensemble risk → campaign context → intervention**

</div>

---

## A clearer signal for risky calls.

CallShield AI is a product-oriented Trust & Safety system for understanding harmful calling behavior without losing sight of legitimate communication.

It combines **transcript NLP, nonlinear behavioral modeling, spoofing and acoustic-style indicators, unsupervised anomaly detection, campaign intelligence, model evaluation, and proportional enforcement** across one synthetic consumer-calling ecosystem.

<p align="center">
  <img src="assets/dashboard-preview.svg" alt="CallShield AI command center" width="100%" />
</p>

> **Command Center:** detection quality, ecosystem health, user protection, emerging-abuse signals, model quality, scam taxonomy, and analyst investigations in one surface.

---

## 18 executive KPIs

The dashboard is organized around three decision layers instead of one flat metric list.

| Detection quality | Protection & ecosystem | Emerging abuse signals |
|---|---|---|
| Scam prevalence | Blocked calls | Campaign candidates |
| Detection recall | Call-screen rate | Repeated-script rate |
| Precision | Spoof-signal rate | Credential-request rate |
| False-positive rate | Robotic-call rate | Payment-request rate |
| PR-AUC | Average recipient reach | Reported-call rate |
| High-risk traffic | Users protected | New-number high-risk rate |

The operating threshold is optimized under a **≤2% false-positive guardrail**, because a calling-safety system has to balance abuse prevention with legitimate-call continuity.

---

## What CallShield detects

```text
LEGITIMATE
ROBOCALL
TELEMARKETING
BANK IMPERSONATION
TECH SUPPORT SCAM
GOVERNMENT IMPERSONATION
ACCOUNT TAKEOVER SCAM
INVESTMENT / CRYPTO SCAM
```

The system does not rely on transcript text alone. A suspicious call can accumulate risk from multiple independent signal families.

| Signal family | Examples |
|---|---|
| **Transcript intelligence** | urgency, credential requests, payment language, repeated scripts |
| **Behavioral ML** | calls/hour, recipient fan-out, prior reports, duration |
| **Identity / spoofing** | new number, spoof indicator |
| **Acoustic proxy** | robotic-voice score |
| **Campaign context** | repetition, fan-out, report concentration, caller-level risk |
| **Novelty detection** | behavior outside the learned legitimate baseline |

---

## 🧠 ML Model Lab

CallShield includes a separate advanced-modeling layer for comparing supervised, unsupervised, and ensemble approaches.

```text
Transcript + numeric baseline ───────────────► Logistic model

Behavioral features ─► XGBoost ─────────────┐
                                            │
Legitimate baseline ─► Isolation Forest ────┼──► Ensemble Champion Score
                                            │
                                            ▼
                               threshold under ≤2% FPR
                                            │
                                            ▼
             ALLOW → LABEL → CALL SCREEN → SILENCE → BLOCK
```

### Model portfolio

| Model | Role |
|---|---|
| **Logistic + TF-IDF baseline** | transparent benchmark using transcript + numeric features |
| **XGBoost behavioral model** | nonlinear interactions across velocity, fan-out, reports, spoofing, urgency, acoustic proxy, and recovery/payment cues |
| **Isolation Forest** | novelty detection for behavior outside the legitimate baseline |
| **Ensemble Champion** | combines supervised risk and anomaly sensitivity into one production-oriented score |

All models are compared using **PR-AUC, ROC-AUC, precision, recall, false-positive rate, and operating threshold** on the same holdout sample.

The Model Lab also includes ranked feature importance and a per-call surface showing **behavioral ML score vs anomaly score vs ensemble score**.

---

## Product decisioning

Prediction is deliberately separated from user-facing action.

```text
ALLOW
  ↓
LABEL SUSPECTED SPAM
  ↓
CALL SCREEN
  ↓
SILENCE
  ↓
BLOCK
```

This makes it possible to tune policy independently from the model and use less disruptive interventions when uncertainty is higher.

---

## Dashboard surfaces

1. **Command Center** — executive health, 18 KPIs, risk distribution, scam taxonomy, investigation queue
2. **Scam Intelligence** — scam classes, transcript cues, and behavioral indicators
3. **Campaign Intelligence** — coordinated caller activity and campaign-risk ranking
4. **Intervention Policy** — allow / label / screen / silence / block decisions
5. **ML Model Lab** — champion-vs-baseline comparison, anomaly detection, feature importance, per-call ensemble analysis

---

## Repository architecture

```text
-CallShield-AI/
├── assets/
│   └── dashboard-preview.svg
├── dashboard/
│   ├── app.py
│   └── pages/
│       ├── 1_Scam_Intelligence.py
│       ├── 2_Campaign_Intelligence.py
│       ├── 3_Intervention_Policy.py
│       └── 4_ML_Model_Lab.py
├── src/
│   ├── generate_data.py
│   ├── features.py
│   ├── model.py
│   ├── model_lab.py
│   ├── campaigns.py
│   ├── interventions.py
│   └── run_pipeline.py
├── tests/
│   └── test_pipeline.py
├── .streamlit/
│   └── config.toml
├── requirements.txt
└── README.md
```

---

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

---

## Production evolution

A real deployment could add **multilingual ASR, transformer transcript embeddings, speaker embeddings, SHAP explanations, STIR/SHAKEN attestation, carrier reputation, device/number graph features, temporal graph neural networks, sequence modeling, region-specific calibration, analyst feedback loops, challenger-vs-champion monitoring, and privacy-preserving aggregation**.

---

<div align="center">

### Protect people from harmful calls without disrupting legitimate communication.

**Voice Safety · NLP · XGBoost · Anomaly Detection · Ensemble ML · Campaign Detection · Policy Decisioning**

</div>
