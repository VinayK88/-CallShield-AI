from pathlib import Path
import sys
import pandas as pd
import streamlit as st

DASH=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(DASH))
from ui import apply_theme, hero, section, kicker, callout

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs'
st.set_page_config(page_title='Campaign Intelligence',page_icon='◎',layout='wide')
apply_theme()

c=pd.read_csv(OUT/'campaigns.csv')
hero('CallShield AI · Campaign Intelligence','See the campaign<br/>behind the call.','Surface coordinated callers using recipient fan-out, model risk, reports, script repetition, spoofing, and scam concentration.',('Fan-out','Repeated scripts','Spoofing','Reports','Campaign risk'))

high=int((c.campaign_risk>=.70).sum()); avg=float(c.campaign_risk.mean()); top=float(c.campaign_risk.max()); reach=int(c.recipients.max()); reports=int(c.reports.max()); repeat=float(c.repeat_similarity.mean())
kicker('Campaign health')
cols=st.columns(6)
for col,l,v in zip(cols,['High-risk candidates','Avg campaign risk','Top campaign risk','Max recipient reach','Max reports','Avg script similarity'],[f'{high:,}',f'{avg:.2f}',f'{top:.2f}',f'{reach:,}',f'{reports:,}',f'{repeat:.1%}']): col.metric(l,v)

callout('Coordinated abuse','One caller can look ordinary. A campaign does not.','Campaign scoring aggregates behavior across calls so broad fan-out, repeated scripts, concentrated reports, spoofing, and model risk become visible at the caller level.')

left,right=st.columns([1.05,.95],gap='large')
with left:
    section('Highest-risk callers.','The top campaign candidates ranked by the combined campaign-risk score.')
    st.bar_chart(c.head(20).set_index('caller_id')['campaign_risk'],height=380)
with right:
    section('Reach versus risk.','A compact analyst view of callers whose recipient reach and risk rise together.')
    view=c.sort_values('campaign_risk',ascending=False).head(20).set_index('caller_id')[['recipients','reports']]
    st.bar_chart(view,height=380)

st.divider(); section('Campaign investigation queue.','Caller-level evidence for coordinated-abuse review and prioritization.')
st.dataframe(c.head(60),use_container_width=True,hide_index=True)
