from pathlib import Path
import json
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs"

st.set_page_config(page_title="ML Model Lab", page_icon="🧠", layout="wide")
st.markdown("""
<style>
html, body, [class*="css"] {font-family:"Avenir Next",Avenir,"Helvetica Neue",Helvetica,Arial,sans-serif;color:#1d1d1f}
.stApp{background:#fff}.block-container{max-width:1420px;padding-top:2.4rem;padding-bottom:4rem}
[data-testid="stSidebar"]{background:#f5f5f7;border-right:1px solid #e8e8ed}
[data-testid="stMetric"]{background:#f5f5f7;border:1px solid #ececf0;border-radius:24px;padding:1.1rem 1.2rem;min-height:116px}
[data-testid="stMetricLabel"]{font-size:.74rem;color:#6e6e73;font-weight:600}
[data-testid="stMetricValue"]{font-size:1.9rem;color:#1d1d1f;font-weight:650;letter-spacing:-.035em}
.lab-eyebrow{color:#0071e3;font-size:.76rem;font-weight:700;letter-spacing:.10em;text-transform:uppercase;margin-bottom:.6rem}
.lab-hero{font-size:3.1rem;line-height:1.04;font-weight:650;letter-spacing:-.048em;color:#1d1d1f;margin:0}
.lab-sub{font-size:1.05rem;line-height:1.55;max-width:900px;color:#6e6e73;margin-top:.85rem}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="lab-eyebrow">CallShield AI · ML Model Lab</div>', unsafe_allow_html=True)
st.markdown('<div class="lab-hero">Compare, explain, and select the champion model.</div>', unsafe_allow_html=True)
st.markdown('<div class="lab-sub">Nonlinear behavioral modeling, novelty detection, ensemble scoring, threshold optimization under a ≤2% false-positive guardrail, and feature-level explainability.</div>', unsafe_allow_html=True)

try:
    comp = pd.read_csv(OUT / "model_comparison.csv")
    imp = pd.read_csv(OUT / "feature_importance.csv")
    scored = pd.read_csv(OUT / "ml_lab_scored.csv")
    summary = json.loads((OUT / "ml_lab_summary.json").read_text())
except FileNotFoundError:
    st.warning("Run `python src/run_pipeline.py --rows 30000` to generate ML Model Lab outputs.")
    st.stop()

champ = summary["champion"]
cols = st.columns(6)
cols[0].metric("Champion", champ["model"])
cols[1].metric("PR-AUC", f"{champ['pr_auc']:.3f}")
cols[2].metric("ROC-AUC", f"{champ['roc_auc']:.3f}")
cols[3].metric("Recall", f"{champ['recall']:.1%}")
cols[4].metric("Precision", f"{champ['precision']:.1%}")
cols[5].metric("FPR", f"{champ['false_positive_rate']:.2%}")

st.divider()
left, right = st.columns([1.05, .95], gap="large")
with left:
    st.subheader("Model comparison")
    st.caption("All models are evaluated on the same holdout sample with operating thresholds optimized under the false-positive guardrail.")
    st.dataframe(comp.style.format({
        "pr_auc":"{:.3f}","roc_auc":"{:.3f}","precision":"{:.1%}",
        "recall":"{:.1%}","false_positive_rate":"{:.2%}","threshold":"{:.2f}"
    }), use_container_width=True, hide_index=True)
    chart = comp.set_index("model")[["pr_auc","recall","precision"]]
    st.bar_chart(chart, height=320)
with right:
    st.subheader("Feature importance")
    st.caption("Tree-derived importance for the supervised behavioral model.")
    top = imp.head(10).set_index("feature")
    st.bar_chart(top["importance"], height=420)

st.subheader("Ensemble investigation surface")
st.caption("Compare supervised behavioral score, anomaly score, and final ensemble score on the highest-risk calls.")
show_cols = [
    "call_id","caller_id","scam_type","behavioral_ml_score","anomaly_score",
    "ensemble_score","prior_reports","unique_recipients_1h","spoof_signal",
    "repeat_script_similarity","robotic_voice_score","transcript"
]
st.dataframe(scored.sort_values("ensemble_score", ascending=False).head(50)[show_cols], use_container_width=True, hide_index=True)

st.info("Production extension: add SHAP values for per-call explanations, multilingual transcript embeddings, calibrated segment-specific thresholds, and challenger-vs-champion monitoring.")
