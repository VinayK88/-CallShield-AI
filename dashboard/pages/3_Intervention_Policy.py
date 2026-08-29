from pathlib import Path
import sys
import pandas as pd
import streamlit as st

DASH=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(DASH))
from ui import apply_theme, hero, section, kicker, callout

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs'
st.set_page_config(page_title='Intervention Policy',page_icon='◇',layout='wide')
apply_theme()

df=pd.read_csv(OUT/'scored_calls.csv')
hero('CallShield AI · Intervention Policy','Protect more.<br/>Disrupt less.','Translate calibrated risk into graduated user protection so uncertain calls receive lighter-touch interventions while the clearest abuse is blocked.',('ALLOW','LABEL','CALL SCREEN','SILENCE','BLOCK'))

mix=df['intervention'].value_counts(normalize=True)
kicker('Policy mix')
cols=st.columns(5)
for col,label in zip(cols,['ALLOW','LABEL SUSPECTED SPAM','CALL SCREEN','SILENCE','BLOCK']): col.metric(label,f"{mix.get(label,0):.1%}")

callout('Policy ladder','Prediction and enforcement stay separate.','Model risk informs the decision, but policy determines the user experience. This separation allows thresholds, friction, and operational constraints to change without retraining the classifier.')

section('Intervention distribution.','How the current policy translates the scored population into product actions.')
st.bar_chart(df['intervention'].value_counts(),height=360)

st.divider(); section('Decision review.','Highest-risk calls with the evidence required to understand why a stronger intervention was selected.')
show=['caller_id','scam_type','risk_score','prior_reports','spoof_signal','unique_recipients_1h','repeat_script_similarity','intervention','transcript']
st.dataframe(df.sort_values('risk_score',ascending=False)[show].head(60),use_container_width=True,hide_index=True)
