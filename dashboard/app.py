from pathlib import Path
import json, pandas as pd, streamlit as st, matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'
st.set_page_config(page_title='CallShield AI',page_icon='☎️',layout='wide')
st.markdown('''<style>
html,body,[class*="css"]{font-family:"Avenir Next",Avenir,"Helvetica Neue",Helvetica,Arial,sans-serif;color:#1d1d1f}.stApp{background:#fff}.block-container{max-width:1420px;padding-top:2.5rem;padding-bottom:4rem}[data-testid="stSidebar"]{background:#f5f5f7;border-right:1px solid #e8e8ed}[data-testid="stMetric"]{background:#f5f5f7;border:1px solid #ececf0;border-radius:24px;padding:1.12rem 1.2rem;box-shadow:0 8px 28px rgba(0,0,0,.025);min-height:116px}[data-testid="stMetricLabel"]{font-size:.74rem;color:#6e6e73;font-weight:600}[data-testid="stMetricValue"]{font-size:1.9rem;color:#1d1d1f;letter-spacing:-.035em;font-weight:650}[data-testid="stDataFrame"]{border:1px solid #ececf0;border-radius:20px;overflow:hidden}.eyebrow{color:#0071e3;font-size:.76rem;font-weight:700;letter-spacing:.10em;text-transform:uppercase;margin-bottom:.6rem}.hero{font-size:3.45rem;line-height:1.02;font-weight:650;letter-spacing:-.052em;color:#1d1d1f;margin:0}.sub{font-size:1.14rem;line-height:1.55;max-width:900px;color:#6e6e73;margin-top:.9rem}.chip{display:inline-block;background:#f5f5f7;color:#424245;border-radius:999px;padding:.42rem .78rem;font-size:.74rem;margin:.3rem .32rem .1rem 0;border:1px solid #ececf0}.section{font-size:1.5rem;font-weight:650;letter-spacing:-.03em;color:#1d1d1f;margin-bottom:.18rem}.section-sub{color:#86868b;font-size:.9rem;margin-bottom:1rem}</style>''',unsafe_allow_html=True)
st.markdown('<div class="eyebrow">CallShield AI · Voice Trust & Safety</div>',unsafe_allow_html=True)
st.markdown('<div class="hero">A clearer signal for risky calls.</div>',unsafe_allow_html=True)
st.markdown('<div class="sub">Detect scam calls, robocalls, impersonation, and coordinated calling campaigns using transcript intelligence, caller behavior, acoustic indicators, graph-style fan-out, and proportional interventions.</div>',unsafe_allow_html=True)
st.markdown('<span class="chip">Voice scams</span><span class="chip">Transcript NLP</span><span class="chip">Behavioral risk</span><span class="chip">Campaign intelligence</span><span class="chip">≤2% FPR guardrail</span>',unsafe_allow_html=True)
@st.cache_data
def load():
 return pd.read_csv(OUT/'scored_calls.csv'),pd.read_csv(OUT/'campaigns.csv'),json.loads((OUT/'summary.json').read_text())
try:s,c,summary=load()
except FileNotFoundError: st.warning('Run `python src/run_pipeline.py --rows 30000` first.'); st.stop()
m=summary['model_evaluation']; k=summary['kpis']
r1=st.columns(6)
for col,label,val in zip(r1,['Scam prevalence','Detection recall','Precision','False-positive rate','PR-AUC','High-risk traffic'],[f"{m['scam_prevalence']:.1%}",f"{m['recall']:.1%}",f"{m['precision']:.1%}",f"{m['false_positive_rate']:.2%}",f"{m['pr_auc']:.3f}",f"{k['high_risk_rate']:.1%}"]): col.metric(label,val)
st.write(''); r2=st.columns(6)
for col,label,val in zip(r2,['Blocked calls','Call-screen rate','Spoof-signal rate','Robotic-call rate','Avg recipient reach','Users protected'],[f"{k['blocked_rate']:.1%}",f"{k['screened_rate']:.1%}",f"{k['spoof_rate']:.1%}",f"{k['robotic_call_rate']:.1%}",f"{k['avg_reach']:.1f}",f"{k['estimated_protected_users']:,}"]): col.metric(label,val)
st.divider(); left,right=st.columns([1.05,.95],gap='large')
with left:
 st.markdown('<div class="section">Call risk distribution</div><div class="section-sub">Calibrated separation between legitimate and scam calls.</div>',unsafe_allow_html=True); fig,ax=plt.subplots(figsize=(7.4,4.2)); ax.hist(s.loc[s.is_scam==0,'risk_score'],bins=40,alpha=.65,label='Legitimate'); ax.hist(s.loc[s.is_scam==1,'risk_score'],bins=40,alpha=.65,label='Scam'); ax.axvline(m['threshold'],linestyle='--',label='Operating threshold'); ax.spines[['top','right']].set_visible(False); ax.grid(axis='y',alpha=.12); ax.legend(frameon=False); ax.set_xlabel('Risk score'); ax.set_ylabel('Calls'); st.pyplot(fig,use_container_width=True)
with right:
 st.markdown('<div class="section">Scam taxonomy</div><div class="section-sub">What kinds of abusive calling behavior drive ecosystem risk.</div>',unsafe_allow_html=True); st.bar_chart(s[s.is_scam==1]['scam_type'].value_counts(normalize=True),height=330)
st.write(''); st.markdown('<div class="section">Priority call investigations</div><div class="section-sub">Highest-risk calls with transcript, spoofing, report, velocity, and reach evidence.</div>',unsafe_allow_html=True); cols=['call_id','caller_id','receiver_id','scam_type','risk_score','prior_reports','calls_1h','unique_recipients_1h','spoof_signal','robotic_voice_score','intervention','transcript']; st.dataframe(s.sort_values('risk_score',ascending=False).head(25)[cols],use_container_width=True,hide_index=True)
st.write(''); st.markdown('<div class="section">Coordinated calling campaigns</div><div class="section-sub">Caller-level campaign risk from fan-out, reports, script repetition, spoofing, and model risk.</div>',unsafe_allow_html=True); st.dataframe(c.head(20),use_container_width=True,hide_index=True)
