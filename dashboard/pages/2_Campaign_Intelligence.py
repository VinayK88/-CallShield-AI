from pathlib import Path
import pandas as pd, streamlit as st
ROOT=Path(__file__).resolve().parents[2]; c=pd.read_csv(ROOT/'outputs/campaigns.csv')
st.title('Campaign Intelligence'); st.caption('Coordinated caller behavior ranked by fan-out, reports, spoofing, and script repetition.'); st.metric('High-risk campaign candidates',int((c.campaign_risk>=.70).sum())); st.bar_chart(c.head(20).set_index('caller_id')['campaign_risk']); st.dataframe(c.head(50),use_container_width=True,hide_index=True)
