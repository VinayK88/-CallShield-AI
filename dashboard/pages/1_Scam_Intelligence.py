from pathlib import Path
import sys
import pandas as pd
import streamlit as st

DASH=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(DASH))
from ui import apply_theme, hero, section, kicker, callout

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs'
st.set_page_config(page_title='Scam Intelligence',page_icon='◉',layout='wide')
apply_theme()

df=pd.read_csv(OUT/'scored_calls.csv')
hero('CallShield AI · Scam Intelligence','Understand the pattern.<br/>Not just the score.','Explore scam taxonomy, transcript cues, spoofing, behavioral velocity, acoustic-style signals, and user reports behind harmful-call risk.',('Taxonomy','Transcript signals','Behavioral ML','Spoofing','Robocall signals'))

scam=df[df.is_scam==1]
known=int(scam['scam_type'].nunique()); reported=float((df.prior_reports>0).mean()); spoof=float(df.spoof_signal.mean()); robotic=float((df.robotic_voice_score>=.60).mean()); cred=float(df.credential_request.mean()); pay=float(df.payment_request.mean())
kicker('Ecosystem signals')
cols=st.columns(6)
for c,l,v in zip(cols,['Known scam classes','Reported calls','Spoof signal','Robotic calls','Credential requests','Payment requests'],[f'{known}',f'{reported:.1%}',f'{spoof:.1%}',f'{robotic:.1%}',f'{cred:.1%}',f'{pay:.1%}']): c.metric(l,v)

callout('Intelligence layer','From category to evidence.','The page combines model risk with interpretable evidence so investigators can see whether a call looks like bank impersonation, account takeover, robocalling, tech-support fraud, or another abuse pattern.')

left,right=st.columns([1,.9],gap='large')
with left:
    section('Scam mix.','Relative prevalence of known harmful-call classes in the synthetic evaluation population.')
    st.bar_chart(scam['scam_type'].value_counts(normalize=True),height=360)
with right:
    section('Risk by scam class.','Average model risk by abuse category reveals which classes the system separates most strongly.')
    avg=scam.groupby('scam_type')['risk_score'].mean().sort_values(ascending=False)
    st.bar_chart(avg,height=360)

st.divider(); section('High-risk evidence.','Prioritized calls with text, behavioral, identity, and acoustic-style indicators in one surface.')
show=['call_id','caller_id','scam_type','risk_score','calls_1h','unique_recipients_1h','prior_reports','spoof_signal','repeat_script_similarity','robotic_voice_score','credential_request','payment_request','intervention','transcript']
st.dataframe(df.sort_values('risk_score',ascending=False).head(60)[show],use_container_width=True,hide_index=True)
