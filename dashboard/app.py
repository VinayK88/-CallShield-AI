from pathlib import Path
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from ui import apply_theme, hero, section, kicker, callout

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'
st.set_page_config(page_title='CallShield AI',page_icon='☎️',layout='wide')
apply_theme()

hero(
    'CallShield AI · Voice Trust & Safety',
    "Know when a call<br/>doesn't feel right.",
    'A voice-safety intelligence platform for detecting scam calls, understanding coordinated abuse, explaining model risk, and choosing the least disruptive intervention that still protects the user.',
    ('Transcript NLP','XGBoost','Isolation Forest','Ensemble Risk','SHAP-ready Explainability','≤2% FPR Guardrail')
)

@st.cache_data
def load():
    return pd.read_csv(OUT/'scored_calls.csv'), pd.read_csv(OUT/'campaigns.csv'), json.loads((OUT/'summary.json').read_text())

try:
    s,c,summary=load()
except FileNotFoundError:
    st.warning('Run `python src/run_pipeline.py --rows 30000` first.')
    st.stop()

m=summary['model_evaluation']; k=summary['kpis']
campaign_candidates=int((c['campaign_risk']>=.70).sum()) if 'campaign_risk' in c else 0
high_repeat=float((s['repeat_script_similarity']>=.75).mean())
credential_rate=float(s['credential_request'].mean())
payment_rate=float(s['payment_request'].mean())
reported_rate=float((s['prior_reports']>0).mean())
novelty_proxy=float(((s['new_number']==1)&(s['risk_score']>=.70)).mean())

callout('Model champion','Protection without over-blocking.','The operating threshold is tuned to maximize harmful-call recall while keeping legitimate-call false positives within a strict ≤2% guardrail. Risk is translated into graduated product actions: allow, label, call screen, silence, or block.')

kicker('Detection quality')
r1=st.columns(6)
for col,label,val in zip(r1,['Scam prevalence','Detection recall','Precision','False-positive rate','PR-AUC','High-risk traffic'],[f"{m['scam_prevalence']:.1%}",f"{m['recall']:.1%}",f"{m['precision']:.1%}",f"{m['false_positive_rate']:.2%}",f"{m['pr_auc']:.3f}",f"{k['high_risk_rate']:.1%}"]): col.metric(label,val)

kicker('Protection & ecosystem')
r2=st.columns(6)
for col,label,val in zip(r2,['Blocked calls','Call-screen rate','Spoof-signal rate','Robotic-call rate','Avg recipient reach','Users protected'],[f"{k['blocked_rate']:.1%}",f"{k['screened_rate']:.1%}",f"{k['spoof_rate']:.1%}",f"{k['robotic_call_rate']:.1%}",f"{k['avg_reach']:.1f}",f"{k['estimated_protected_users']:,}"]): col.metric(label,val)

kicker('Emerging abuse signals')
r3=st.columns(6)
for col,label,val in zip(r3,['Campaign candidates','Repeated-script rate','Credential-request rate','Payment-request rate','Reported-call rate','New-number high risk'],[f"{campaign_candidates:,}",f"{high_repeat:.1%}",f"{credential_rate:.1%}",f"{payment_rate:.1%}",f"{reported_rate:.1%}",f"{novelty_proxy:.1%}"]): col.metric(label,val)

st.divider()
left,right=st.columns([1.05,.95],gap='large')
with left:
    section('Risk, made visible.','Calibrated separation between legitimate and scam calls under the production guardrail.')
    fig,ax=plt.subplots(figsize=(7.4,4.2)); fig.patch.set_facecolor('white'); ax.set_facecolor('white')
    ax.hist(s.loc[s.is_scam==0,'risk_score'],bins=40,alpha=.62,label='Legitimate')
    ax.hist(s.loc[s.is_scam==1,'risk_score'],bins=40,alpha=.62,label='Scam')
    ax.axvline(m['threshold'],linestyle='--',linewidth=1.35,label='Operating threshold')
    ax.spines[['top','right']].set_visible(False); ax.spines[['left','bottom']].set_alpha(.16); ax.grid(axis='y',alpha=.07); ax.legend(frameon=False)
    ax.set_xlabel('Risk score'); ax.set_ylabel('Calls'); st.pyplot(fig,use_container_width=True)
with right:
    section("See what's changing.",'The scam taxonomy surfaces which abuse categories contribute most to ecosystem risk.')
    st.bar_chart(s[s.is_scam==1]['scam_type'].value_counts(normalize=True),height=330)

st.write(''); section('The calls that need attention.','Highest-risk events with transcript, spoofing, reports, velocity, reach, and intervention evidence in one analyst surface.')
cols=['call_id','caller_id','receiver_id','scam_type','risk_score','prior_reports','calls_1h','unique_recipients_1h','spoof_signal','robotic_voice_score','intervention','transcript']
st.dataframe(s.sort_values('risk_score',ascending=False).head(25)[cols],use_container_width=True,hide_index=True)

st.write(''); section('Campaigns, not just calls.','Caller-level campaign risk combines fan-out, reports, repeated scripts, spoofing, and model risk to surface coordinated abuse.')
st.dataframe(c.head(20),use_container_width=True,hide_index=True)
