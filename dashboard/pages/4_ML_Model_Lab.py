from pathlib import Path
import sys, json
import pandas as pd
import streamlit as st

DASH=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(DASH))
from ui import apply_theme, hero, section, kicker, callout

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs'
st.set_page_config(page_title='ML Model Lab',page_icon='◌',layout='wide')
apply_theme()

hero('CallShield AI · ML Model Lab','Compare. Explain.<br/>Choose the champion.','Evaluate supervised, unsupervised, and ensemble approaches under the same holdout population and a strict false-positive guardrail.',('Logistic + TF-IDF','XGBoost','Isolation Forest','Ensemble champion','Explainability'))

try:
    comp=pd.read_csv(OUT/'model_comparison.csv')
    imp=pd.read_csv(OUT/'feature_importance.csv')
    scored=pd.read_csv(OUT/'ml_lab_scored.csv')
    summary=json.loads((OUT/'ml_lab_summary.json').read_text())
except FileNotFoundError:
    st.warning('Run `python src/run_pipeline.py --rows 30000` to generate ML Model Lab outputs.')
    st.stop()

champ=summary['champion']
kicker('Champion model')
cols=st.columns(6)
for col,label,val in zip(cols,['Champion','PR-AUC','ROC-AUC','Recall','Precision','FPR'],[champ['model'],f"{champ['pr_auc']:.3f}",f"{champ['roc_auc']:.3f}",f"{champ['recall']:.1%}",f"{champ['precision']:.1%}",f"{champ['false_positive_rate']:.2%}"]): col.metric(label,val)

callout('Model selection','Better means useful under the product constraint.','Every candidate is evaluated on the same holdout set, then thresholded under the false-positive guardrail. The champion is selected for balanced abuse coverage, legitimate-call protection, and operational usefulness—not headline accuracy alone.')

left,right=st.columns([1.05,.95],gap='large')
with left:
    section('Model comparison.','PR-AUC, precision, recall, ROC-AUC, FPR, and threshold on a common holdout population.')
    st.dataframe(comp.style.format({'pr_auc':'{:.3f}','roc_auc':'{:.3f}','precision':'{:.1%}','recall':'{:.1%}','false_positive_rate':'{:.2%}','threshold':'{:.2f}'}),use_container_width=True,hide_index=True)
    st.bar_chart(comp.set_index('model')[['pr_auc','recall','precision']],height=320)
with right:
    section('What drives the model?','Ranked tree-derived feature importance for the supervised behavioral model.')
    st.bar_chart(imp.head(12).set_index('feature')['importance'],height=430)

st.divider(); section('Ensemble investigation surface.','Compare behavioral ML, novelty, and final ensemble risk on the calls most likely to need analyst attention.')
show=['call_id','caller_id','scam_type','behavioral_ml_score','anomaly_score','ensemble_score','prior_reports','unique_recipients_1h','spoof_signal','repeat_script_similarity','robotic_voice_score','transcript']
st.dataframe(scored.sort_values('ensemble_score',ascending=False).head(60)[show],use_container_width=True,hide_index=True)

st.info('Production extension: native per-call SHAP values, multilingual transcript embeddings, calibrated segment thresholds, and challenger-vs-champion monitoring.')
