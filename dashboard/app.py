from pathlib import Path
import json, pandas as pd, streamlit as st, matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'
st.set_page_config(page_title='CallShield AI',page_icon='☎️',layout='wide')
st.markdown('''<style>
html,body,[class*="css"]{font-family:"Avenir Next",Avenir,"Helvetica Neue",Helvetica,Arial,sans-serif;color:#1d1d1f}.stApp{background:#fff}.block-container{max-width:1440px;padding-top:2.7rem;padding-bottom:4.5rem}[data-testid="stSidebar"]{background:#f5f5f7;border-right:1px solid #e8e8ed}[data-testid="stMetric"]{background:#f5f5f7;border:1px solid #ececf0;border-radius:24px;padding:1.12rem 1.2rem;box-shadow:0 8px 28px rgba(0,0,0,.025);min-height:116px}[data-testid="stMetricLabel"]{font-size:.73rem;color:#6e6e73;font-weight:600;letter-spacing:.01em}[data-testid="stMetricValue"]{font-size:1.92rem;color:#1d1d1f;letter-spacing:-.035em;font-weight:650}[data-testid="stMetricDelta"]{font-size:.70rem}[data-testid="stDataFrame"]{border:1px solid #ececf0;border-radius:20px;overflow:hidden}.eyebrow{color:#0071e3;font-size:.76rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin-bottom:.65rem}.hero{font-size:3.65rem;line-height:1.01;font-weight:650;letter-spacing:-.055em;color:#1d1d1f;margin:0}.sub{font-size:1.14rem;line-height:1.58;max-width:930px;color:#6e6e73;margin-top:1rem}.chip{display:inline-block;background:#f5f5f7;color:#424245;border-radius:999px;padding:.43rem .8rem;font-size:.74rem;margin:.34rem .34rem .12rem 0;border:1px solid #ececf0}.section{font-size:1.52rem;font-weight:650;letter-spacing:-.03em;color:#1d1d1f;margin-bottom:.18rem}.section-sub{color:#86868b;font-size:.9rem;margin-bottom:1rem}.health{display:inline-block;background:#eef8f1;color:#248a3d;border-radius:999px;padding:.42rem .72rem;font-size:.73rem;font-weight:650;margin-top:.6rem}.kicker{font-size:.74rem;color:#86868b;text-transform:uppercase;letter-spacing:.08em;font-weight:700;margin:1.2rem 0 .6rem}</style>''',unsafe_allow_html=True)
st.markdown('<div class="eyebrow">CallShield AI · Voice Trust & Safety</div>',unsafe_allow_html=True)
st.markdown('<div class="hero">A clearer signal for risky calls.</div>',unsafe_allow_html=True)
st.markdown('<div class="sub">Detect scam calls, robocalls, impersonation, and coordinated calling campaigns using transcript intelligence, behavioral ML, novelty detection, campaign context, and proportional interventions.</div>',unsafe_allow_html=True)
st.markdown('<span class="chip">Voice scams</span><span class="chip">Transcript NLP</span><span class="chip">XGBoost</span><span class="chip">Isolation Forest</span><span class="chip">Ensemble risk</span><span class="chip">≤2% FPR guardrail</span><span class="health">● System healthy</span>',unsafe_allow_html=True)
@st.cache_data
def load():
 return pd.read_csv(OUT/'scored_calls.csv'),pd.read_csv(OUT/'campaigns.csv'),json.loads((OUT/'summary.json').read_text())
try:s,c,summary=load()
except FileNotFoundError: st.warning('Run `python src/run_pipeline.py --rows 30000` first.'); st.stop()
m=summary['model_evaluation']; k=summary['kpis']
campaign_candidates=int((c['campaign_risk']>=.70).sum()) if 'campaign_risk' in c else 0
high_repeat=float((s['repeat_script_similarity']>=.75).mean())
credential_rate=float(s['credential_request'].mean())
payment_rate=float(s['payment_request'].mean())
reported_rate=float((s['prior_reports']>0).mean())
novelty_proxy=float(((s['new_number']==1)&(s['risk_score']>=.70)).mean())
st.markdown('<div class="kicker">Detection quality</div>',unsafe_allow_html=True)
r1=st.columns(6)
for col,label,val in zip(r1,['Scam prevalence','Detection recall','Precision','False-positive rate','PR-AUC','High-risk traffic'],[f"{m['scam_prevalence']:.1%}",f"{m['recall']:.1%}",f"{m['precision']:.1%}",f"{m['false_positive_rate']:.2%}",f"{m['pr_auc']:.3f}",f"{k['high_risk_rate']:.1%}"]): col.metric(label,val)
st.markdown('<div class="kicker">Protection & ecosystem</div>',unsafe_allow_html=True)
r2=st.columns(6)
for col,label,val in zip(r2,['Blocked calls','Call-screen rate','Spoof-signal rate','Robotic-call rate','Avg recipient reach','Users protected'],[f"{k['blocked_rate']:.1%}",f"{k['screened_rate']:.1%}",f"{k['spoof_rate']:.1%}",f"{k['robotic_call_rate']:.1%}",f"{k['avg_reach']:.1f}",f"{k['estimated_protected_users']:,}"]): col.metric(label,val)
st.markdown('<div class="kicker">Emerging abuse signals</div>',unsafe_allow_html=True)
r3=st.columns(6)
for col,label,val in zip(r3,['Campaign candidates','Repeated-script rate','Credential-request rate','Payment-request rate','Reported-call rate','New-number high risk'],[f"{campaign_candidates:,}",f"{high_repeat:.1%}",f"{credential_rate:.1%}",f"{payment_rate:.1%}",f"{reported_rate:.1%}",f"{novelty_proxy:.1%}"]): col.metric(label,val)
st.divider(); left,right=st.columns([1.05,.95],gap='large')
with left:
 st.markdown('<div class="section">Call risk distribution</div><div class="section-sub">Calibrated separation between legitimate and scam calls under the production guardrail.</div>',unsafe_allow_html=True); fig,ax=plt.subplots(figsize=(7.4,4.2)); fig.patch.set_facecolor('white'); ax.set_facecolor('white'); ax.hist(s.loc[s.is_scam==0,'risk_score'],bins=40,alpha=.65,label='Legitimate'); ax.hist(s.loc[s.is_scam==1,'risk_score'],bins=40,alpha=.65,label='Scam'); ax.axvline(m['threshold'],linestyle='--',linewidth=1.4,label='Operating threshold'); ax.spines[['top','right']].set_visible(False); ax.spines[['left','bottom']].set_alpha(.18); ax.grid(axis='y',alpha=.10); ax.legend(frameon=False); ax.set_xlabel('Risk score'); ax.set_ylabel('Calls'); st.pyplot(fig,use_container_width=True)
with right:
 st.markdown('<div class="section">Scam taxonomy</div><div class="section-sub">Which abusive calling categories are contributing most to ecosystem risk.</div>',unsafe_allow_html=True); st.bar_chart(s[s.is_scam==1]['scam_type'].value_counts(normalize=True),height=330)
st.write(''); st.markdown('<div class="section">Priority call investigations</div><div class="section-sub">Highest-risk calls with transcript, spoofing, reports, velocity, reach, and intervention evidence.</div>',unsafe_allow_html=True); cols=['call_id','caller_id','receiver_id','scam_type','risk_score','prior_reports','calls_1h','unique_recipients_1h','spoof_signal','robotic_voice_score','intervention','transcript']; st.dataframe(s.sort_values('risk_score',ascending=False).head(25)[cols],use_container_width=True,hide_index=True)
st.write(''); st.markdown('<div class="section">Coordinated calling campaigns</div><div class="section-sub">Caller-level campaign risk from fan-out, reports, repeated scripts, spoofing, and model risk.</div>',unsafe_allow_html=True); st.dataframe(c.head(20),use_container_width=True,hide_index=True)
