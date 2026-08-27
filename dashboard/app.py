from pathlib import Path
import json, pandas as pd, streamlit as st, matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'
st.set_page_config(page_title='CallShield AI',page_icon='☎️',layout='wide')

st.markdown('''
<style>
:root{
  --ink:#1d1d1f;
  --muted:#6e6e73;
  --soft:#f5f5f7;
  --line:#e8e8ed;
  --blue:#0071e3;
  --green:#248a3d;
}
html,body,[class*="css"]{
  font-family:"Avenir Next",Avenir,"Helvetica Neue",Helvetica,Arial,sans-serif;
  color:var(--ink);
}
.stApp{
  background:linear-gradient(180deg,#ffffff 0%,#ffffff 65%,#fafafa 100%);
}
.block-container{
  max-width:1460px;
  padding-top:1.2rem;
  padding-bottom:5rem;
}
[data-testid="stSidebar"]{
  background:rgba(245,245,247,.92);
  backdrop-filter:blur(22px);
  border-right:1px solid rgba(0,0,0,.06);
}
[data-testid="stSidebarNav"] span,
[data-testid="stSidebarNav"] a{
  font-size:.92rem;
}
[data-testid="stMetric"]{
  background:rgba(245,245,247,.82);
  border:1px solid rgba(0,0,0,.04);
  border-radius:28px;
  padding:1.2rem 1.25rem 1.1rem;
  box-shadow:0 12px 34px rgba(0,0,0,.035);
  min-height:122px;
}
[data-testid="stMetric"]:hover{
  transform:translateY(-1px);
  box-shadow:0 16px 38px rgba(0,0,0,.05);
  transition:.18s ease;
}
[data-testid="stMetricLabel"]{
  font-size:.72rem;
  color:var(--muted);
  font-weight:650;
  letter-spacing:.015em;
}
[data-testid="stMetricValue"]{
  font-size:2rem;
  color:var(--ink);
  letter-spacing:-.045em;
  font-weight:650;
}
[data-testid="stMetricDelta"]{font-size:.70rem}
[data-testid="stDataFrame"]{
  border:1px solid var(--line);
  border-radius:24px;
  overflow:hidden;
  box-shadow:0 10px 28px rgba(0,0,0,.025);
}
hr{border-color:var(--line)!important;margin:2.7rem 0!important}

.hero-wrap{
  padding:4.5rem 1.2rem 3.2rem;
  text-align:center;
  max-width:1120px;
  margin:0 auto;
}
.eyebrow{
  color:var(--blue);
  font-size:.78rem;
  font-weight:700;
  letter-spacing:.12em;
  text-transform:uppercase;
  margin-bottom:1rem;
}
.hero{
  font-size:5.15rem;
  line-height:.96;
  font-weight:650;
  letter-spacing:-.072em;
  color:var(--ink);
  margin:0;
}
.sub{
  font-size:1.34rem;
  line-height:1.48;
  max-width:880px;
  color:var(--muted);
  margin:1.45rem auto 0;
  letter-spacing:-.012em;
}
.hero-meta{
  margin-top:1.55rem;
  display:flex;
  flex-wrap:wrap;
  gap:.55rem;
  justify-content:center;
}
.chip{
  display:inline-block;
  background:var(--soft);
  color:#424245;
  border-radius:999px;
  padding:.5rem .86rem;
  font-size:.75rem;
  border:1px solid rgba(0,0,0,.04);
}
.health{
  display:inline-block;
  background:#eff8f1;
  color:var(--green);
  border-radius:999px;
  padding:.5rem .86rem;
  font-size:.75rem;
  font-weight:650;
}
.hero-panel{
  margin:1.2rem 0 3rem;
  padding:2.6rem 3rem;
  border-radius:34px;
  background:linear-gradient(135deg,#f5f5f7 0%,#fbfbfd 100%);
  border:1px solid rgba(0,0,0,.035);
  box-shadow:0 20px 50px rgba(0,0,0,.035);
}
.hero-panel .kicker-small{
  color:var(--blue);
  font-size:.72rem;
  font-weight:700;
  letter-spacing:.09em;
  text-transform:uppercase;
}
.hero-panel .big{
  font-size:2rem;
  line-height:1.12;
  font-weight:650;
  letter-spacing:-.04em;
  margin:.45rem 0 .5rem;
}
.hero-panel .copy{
  color:var(--muted);
  font-size:.97rem;
  line-height:1.55;
  margin:0;
}
.kicker{
  font-size:.72rem;
  color:#86868b;
  text-transform:uppercase;
  letter-spacing:.10em;
  font-weight:700;
  margin:1.5rem 0 .75rem;
}
.section{
  font-size:1.9rem;
  font-weight:650;
  letter-spacing:-.045em;
  color:var(--ink);
  margin-bottom:.25rem;
}
.section-sub{
  color:#86868b;
  font-size:.95rem;
  line-height:1.5;
  margin-bottom:1.2rem;
}
.section-shell{
  background:#fafafa;
  border:1px solid rgba(0,0,0,.035);
  border-radius:30px;
  padding:1.3rem 1.5rem .6rem;
}
@media (max-width:900px){
  .hero{font-size:3.35rem}
  .sub{font-size:1.08rem}
  .hero-wrap{padding-top:2.5rem}
}
</style>
''',unsafe_allow_html=True)

st.markdown('''
<div class="hero-wrap">
  <div class="eyebrow">CallShield AI · Voice Trust & Safety</div>
  <div class="hero">Know when a call<br/>doesn't feel right.</div>
  <div class="sub">A voice-safety intelligence platform for detecting scam calls, understanding coordinated abuse, explaining model risk, and choosing the least disruptive intervention that still protects the user.</div>
  <div class="hero-meta">
    <span class="chip">Transcript NLP</span>
    <span class="chip">XGBoost</span>
    <span class="chip">Isolation Forest</span>
    <span class="chip">Ensemble Risk</span>
    <span class="chip">SHAP-ready Explainability</span>
    <span class="chip">≤2% FPR Guardrail</span>
    <span class="health">● System healthy</span>
  </div>
</div>
''',unsafe_allow_html=True)

@st.cache_data
def load():
    return (
        pd.read_csv(OUT/'scored_calls.csv'),
        pd.read_csv(OUT/'campaigns.csv'),
        json.loads((OUT/'summary.json').read_text())
    )

try:
    s,c,summary=load()
except FileNotFoundError:
    st.warning('Run `python src/run_pipeline.py --rows 30000` first.')
    st.stop()

m=summary['model_evaluation']
k=summary['kpis']
campaign_candidates=int((c['campaign_risk']>=.70).sum()) if 'campaign_risk' in c else 0
high_repeat=float((s['repeat_script_similarity']>=.75).mean())
credential_rate=float(s['credential_request'].mean())
payment_rate=float(s['payment_request'].mean())
reported_rate=float((s['prior_reports']>0).mean())
novelty_proxy=float(((s['new_number']==1)&(s['risk_score']>=.70)).mean())

st.markdown('''
<div class="hero-panel">
  <div class="kicker-small">Model champion</div>
  <div class="big">Protection without over-blocking.</div>
  <p class="copy">The operating threshold is tuned to maximize harmful-call recall while keeping legitimate-call false positives within a strict ≤2% guardrail. Risk is then translated into graduated product actions: allow, label, call screen, silence, or block.</p>
</div>
''',unsafe_allow_html=True)

st.markdown('<div class="kicker">Detection quality</div>',unsafe_allow_html=True)
r1=st.columns(6)
for col,label,val in zip(
    r1,
    ['Scam prevalence','Detection recall','Precision','False-positive rate','PR-AUC','High-risk traffic'],
    [f"{m['scam_prevalence']:.1%}",f"{m['recall']:.1%}",f"{m['precision']:.1%}",f"{m['false_positive_rate']:.2%}",f"{m['pr_auc']:.3f}",f"{k['high_risk_rate']:.1%}"]
):
    col.metric(label,val)

st.markdown('<div class="kicker">Protection & ecosystem</div>',unsafe_allow_html=True)
r2=st.columns(6)
for col,label,val in zip(
    r2,
    ['Blocked calls','Call-screen rate','Spoof-signal rate','Robotic-call rate','Avg recipient reach','Users protected'],
    [f"{k['blocked_rate']:.1%}",f"{k['screened_rate']:.1%}",f"{k['spoof_rate']:.1%}",f"{k['robotic_call_rate']:.1%}",f"{k['avg_reach']:.1f}",f"{k['estimated_protected_users']:,}"]
):
    col.metric(label,val)

st.markdown('<div class="kicker">Emerging abuse signals</div>',unsafe_allow_html=True)
r3=st.columns(6)
for col,label,val in zip(
    r3,
    ['Campaign candidates','Repeated-script rate','Credential-request rate','Payment-request rate','Reported-call rate','New-number high risk'],
    [f"{campaign_candidates:,}",f"{high_repeat:.1%}",f"{credential_rate:.1%}",f"{payment_rate:.1%}",f"{reported_rate:.1%}",f"{novelty_proxy:.1%}"]
):
    col.metric(label,val)

st.divider()
left,right=st.columns([1.05,.95],gap='large')
with left:
    st.markdown('<div class="section">Risk, made visible.</div><div class="section-sub">Calibrated separation between legitimate and scam calls under the production guardrail.</div>',unsafe_allow_html=True)
    fig,ax=plt.subplots(figsize=(7.4,4.2))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.hist(s.loc[s.is_scam==0,'risk_score'],bins=40,alpha=.65,label='Legitimate')
    ax.hist(s.loc[s.is_scam==1,'risk_score'],bins=40,alpha=.65,label='Scam')
    ax.axvline(m['threshold'],linestyle='--',linewidth=1.4,label='Operating threshold')
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_alpha(.16)
    ax.grid(axis='y',alpha=.08)
    ax.legend(frameon=False)
    ax.set_xlabel('Risk score')
    ax.set_ylabel('Calls')
    st.pyplot(fig,use_container_width=True)
with right:
    st.markdown('<div class="section">See what's changing.</div><div class="section-sub">The scam taxonomy surfaces which abuse categories contribute most to ecosystem risk.</div>',unsafe_allow_html=True)
    st.bar_chart(s[s.is_scam==1]['scam_type'].value_counts(normalize=True),height=330)

st.write('')
st.markdown('<div class="section">The calls that need attention.</div><div class="section-sub">Highest-risk events with transcript, spoofing, reports, velocity, reach, and intervention evidence in one analyst surface.</div>',unsafe_allow_html=True)
cols=['call_id','caller_id','receiver_id','scam_type','risk_score','prior_reports','calls_1h','unique_recipients_1h','spoof_signal','robotic_voice_score','intervention','transcript']
st.dataframe(s.sort_values('risk_score',ascending=False).head(25)[cols],use_container_width=True,hide_index=True)

st.write('')
st.markdown('<div class="section">Campaigns, not just calls.</div><div class="section-sub">Caller-level campaign risk combines fan-out, reports, repeated scripts, spoofing, and model risk to surface coordinated abuse.</div>',unsafe_allow_html=True)
st.dataframe(c.head(20),use_container_width=True,hide_index=True)
