<div align="center">

# ☎️ CallShield AI

### Voice Scam & Spam Call Intelligence Platform

**Scam Detection · Transcript NLP · Behavioral Risk · Acoustic Indicators · Campaign Intelligence · Intervention Policy**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Multi--Page%20Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Risk%20Model-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Trust & Safety](https://img.shields.io/badge/Trust%20%26%20Safety-Voice%20Calls-238636?style=flat-square)](#)

**call → transcript intelligence → behavioral signals → acoustic indicators → risk score → campaign context → intervention**

</div>

---

## 📊 Dashboard preview

<p align="center"><img src="assets/dashboard-preview.svg" alt="CallShield AI dashboard preview" width="100%" /></p>

> Executive and analyst view of scam prevalence, model quality, spoofing, robotic-call activity, user protection, campaign risk, and intervention decisions.

---

## Product concept

CallShield AI is a portfolio-grade Trust & Safety data science platform for protecting a consumer calling ecosystem from **robocalls, telemarketing abuse, bank impersonation, tech-support scams, government impersonation, account-takeover scams, and investment scams**.

The project combines **transcript NLP, caller behavior, acoustic-style indicators, spoofing signals, campaign intelligence, proportional interventions, and operational KPI monitoring**. All data is synthetic.

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

The model selects an operating threshold to maximize scam recall while keeping false-positive rate near a strict **≤2% guardrail**.

## Intervention ladder

`ALLOW → LABEL SUSPECTED SPAM → CALL SCREEN → SILENCE → BLOCK`

## Executive KPIs

**Scam prevalence · Detection recall · Precision · False-positive rate · PR-AUC · High-risk traffic · Blocked calls · Call-screen rate · Spoof-signal rate · Robotic-call rate · Average recipient reach · Estimated users protected**

## Multi-page dashboard

1. `dashboard/app.py` — **Command Center**
2. `dashboard/pages/1_Scam_Intelligence.py` — **Scam Intelligence**
3. `dashboard/pages/2_Campaign_Intelligence.py` — **Campaign Intelligence**
4. `dashboard/pages/3_Intervention_Policy.py` — **Intervention Policy**

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_pipeline.py --rows 30000
streamlit run dashboard/app.py
```

## Production evolution

A real system could add **speech embeddings, multilingual ASR, speaker embeddings, STIR/SHAKEN attestation, carrier reputation, device/number graph features, temporal graph neural networks, sequence models, calibrated market-specific thresholds, analyst feedback loops, and privacy-preserving aggregation**.

---

<div align="center">

### Protect people from harmful calls without disrupting legitimate communication.

**Voice Safety · NLP · Behavioral ML · Campaign Detection · Policy Decisioning**

</div>
