<div align="center">

# ☎️ CallShield AI

### Voice Trust & Safety Intelligence

**Detect harmful calls. Explain the risk. Apply the right intervention.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Product%20Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Behavioral%20ML-EC6B23?style=flat-square)](https://xgboost.ai/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Anomaly%20Detection-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Explainability](https://img.shields.io/badge/Explainability-SHAP-0071E3?style=flat-square)](#explainable-risk)
[![Trust & Safety](https://img.shields.io/badge/Trust%20%26%20Safety-Voice%20Calls-238636?style=flat-square)](#)

`Transcript NLP` · `Behavioral ML` · `Anomaly Detection` · `Ensemble Risk` · `SHAP` · `Campaign Intelligence`

</div>

---

## A clearer signal for risky calls.

CallShield AI is an end-to-end **voice Trust & Safety data science platform** designed to identify scam calls, understand coordinated abuse, explain model decisions, and translate risk into proportional product interventions.

Instead of treating every call as an isolated classification problem, CallShield combines **what was said, how the caller behaves, how widely the caller is reaching, whether the activity looks anomalous, and whether the caller resembles a coordinated campaign**.

<p align="center">
  <img src="assets/dashboard-preview.svg" alt="CallShield AI Command Center with KPI monitoring, ML champion health, and SHAP explainability" width="100%" />
</p>

<p align="center"><sub>Command Center · synthetic portfolio demonstration</sub></p>

---

## Product objectives

| Objective | Product question |
|---|---|
| **Detect** | Is this call likely to be harmful? |
| **Understand** | What scam pattern or campaign does it resemble? |
| **Explain** | Which signals drove the model's risk estimate? |
| **Protect** | Should the experience allow, label, screen, silence, or block? |
| **Measure** | Are protections reducing abuse without disrupting legitimate calls? |

---

## 18 ecosystem KPIs

The Command Center groups metrics by the decision they support rather than presenting one flat monitoring wall.

| Detection quality | Protection & ecosystem | Emerging abuse signals |
|---|---|---|
| Scam prevalence | Blocked calls | Campaign candidates |
| Detection recall | Call-screen rate | Repeated-script rate |
| Precision | Spoof-signal rate | Credential-request rate |
| False-positive rate | Robotic-call rate | Payment-request rate |
| PR-AUC | Average recipient reach | Reported-call rate |
| High-risk traffic | Users protected | New-number high-risk rate |

**Primary product guardrail:** false-positive rate **≤2%** at the selected operating threshold.

That constraint matters because an anti-abuse model is not successful if it protects users by aggressively disrupting legitimate communication.

---

## Abuse taxonomy

```text
LEGITIMATE
├── Personal / expected communication
└── Transactional / service communication

UNWANTED OR HARMFUL
├── Robocall
├── Telemarketing
├── Bank impersonation
├── Tech-support scam
├── Government impersonation
├── Account-takeover scam
└── Investment / crypto scam
```

---

## Signal intelligence

A call can accumulate risk from multiple independent signal families.

| Signal family | Example features | Why it matters |
|---|---|---|
| **Transcript intelligence** | urgency, credential requests, payment language | identifies social-engineering intent |
| **Behavioral ML** | calls/hour, recipient fan-out, reports, duration | detects abnormal caller behavior |
| **Identity / spoofing** | new number, spoof indicator | captures caller-identity uncertainty |
| **Acoustic proxy** | robotic-voice score | supports robocall detection |
| **Campaign context** | repeated scripts, reach, report concentration | surfaces coordinated abuse |
| **Novelty detection** | distance from legitimate behavioral baseline | catches patterns outside known scam labels |

---

## 🧠 ML Model Lab

CallShield uses multiple modeling perspectives rather than relying on a single classifier.

```text
                    CALL EVENT
                        │
          ┌─────────────┴─────────────┐
          │                           │
 transcript + numeric             behavior
          │                           │
 Logistic + TF-IDF                 XGBoost
          │                           │
          │                ┌──────────┘
          │                │
 legitimate baseline ─► Isolation Forest
          │                │
          └────────┬───────┘
                   ▼
           ENSEMBLE RISK SCORE
                   │
          threshold ≤2% FPR
             ┌─────┴─────┐
             ▼           ▼
      SHAP explanation   policy engine
             │           │
             └─────┬─────┘
                   ▼
            analyst context
```

### Model portfolio

| Model | Purpose |
|---|---|
| **Logistic + TF-IDF** | interpretable transcript + numeric baseline |
| **XGBoost** | nonlinear behavioral risk interactions |
| **Isolation Forest** | unseen / novel behavioral anomaly detection |
| **Ensemble Champion** | production-oriented combined risk score |

Models are evaluated on the same holdout population using **PR-AUC, ROC-AUC, precision, recall, false-positive rate, and operating threshold**.

---

<a id="explainable-risk"></a>
## 🔎 Explainable risk

A risk score should answer more than **“how risky?”** It should also help answer **“why?”**

The dashboard preview includes a SHAP-style local explanation for a high-risk bank-impersonation example:

```text
CALLER       caller_00118
RISK         0.982
CLASS        BANK IMPERSONATION
ACTION       BLOCK

Signals increasing risk
credential_request       +0.31  ██████████████████████████
unique_recipients_1h     +0.22  ██████████████████
spoof_signal             +0.17  ██████████████
repeat_script_similarity +0.11  █████████
after_hours_velocity     +0.07  ██████

Signals reducing risk
number_age               -0.08  ███████
normal_duration          -0.05  ████
```

### Analyst interpretation

> **Credential-request language, rapid recipient fan-out, and spoofing are the strongest contributors pushing this call toward scam risk. Lower-risk duration and number-age signals partially offset the score but are not sufficient to change the decision.**

This explanation layer is intended to support **investigation, model validation, false-positive review, policy tuning, and stakeholder communication**.

> **Implementation note:** the current model lab exposes ranked tree feature importance. The README SHAP surface represents the intended per-call explainability extension for the XGBoost champion rather than claiming native SHAP values are already generated by the pipeline.

---

## From model score to product action

Prediction and enforcement are deliberately separated.

```text
LOW RISK                                                   HIGH RISK
   │                                                           │
   ▼                                                           ▼
 ALLOW → LABEL SUSPECTED SPAM → CALL SCREEN → SILENCE → BLOCK
```

This lets policy teams change the user experience without retraining the underlying model and enables less disruptive interventions for uncertain cases.

---

## Campaign intelligence

Individual call risk is only one layer of the problem. CallShield also aggregates caller activity to identify coordinated behavior using:

`recipient fan-out` · `average model risk` · `report volume` · `script repetition` · `spoof rate` · `observed scam concentration`

The result is a caller-level **campaign risk score** that helps prioritize emerging abuse clusters for investigation.

---

## Dashboard surfaces

| Surface | Purpose |
|---|---|
| **Command Center** | 18 KPIs, model health, risk distribution, SHAP-style explanation, priority investigations |
| **Scam Intelligence** | taxonomy, transcripts, behavioral indicators, high-risk events |
| **Campaign Intelligence** | coordinated caller activity and campaign ranking |
| **Intervention Policy** | allow / label / screen / silence / block distribution |
| **ML Model Lab** | champion-vs-baseline evaluation, anomaly scores, feature importance, ensemble analysis |

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

### Generated artifacts

```text
outputs/scored_calls.csv
outputs/campaigns.csv
outputs/ml_lab_scored.csv
outputs/model_comparison.csv
outputs/feature_importance.csv
outputs/ml_lab_summary.json
```

---

## Evaluation philosophy

CallShield treats model quality as a **product tradeoff**, not simply an accuracy problem.

```text
maximize harmful-call recall
            │
            ▼
subject to legitimate-call disruption ≤ acceptable guardrail
            │
            ▼
compare candidate models
            │
            ▼
select champion threshold
            │
            ▼
monitor precision · recall · PR-AUC · FPR · ecosystem impact
```

This mirrors how a consumer-facing safety system would need to balance protection, friction, and trust.

---

## Production evolution

A production implementation could extend the platform with **multilingual ASR, transformer transcript embeddings, speaker embeddings, native per-call SHAP values, STIR/SHAKEN attestation, carrier reputation, device/number graphs, temporal graph neural networks, sequence modeling, market-specific calibration, drift monitoring, analyst feedback loops, challenger-vs-champion deployment, and privacy-preserving aggregation**.

---

## Data & scope

All callers, recipients, transcripts, reports, acoustic indicators, and outcomes in this repository are **synthetic**. The project is designed to demonstrate applied data science, Trust & Safety measurement, ML evaluation, explainability, and product decisioning—not to represent a production telecom dataset.

---

<div align="center">

### Protect people from harmful calls without disrupting legitimate communication.

**Voice Safety · NLP · Behavioral ML · XGBoost · Anomaly Detection · SHAP · Campaign Intelligence · Product Measurement**

</div>