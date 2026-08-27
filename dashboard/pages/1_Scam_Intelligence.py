from pathlib import Path
import pandas as pd, streamlit as st
ROOT=Path(__file__).resolve().parents[2]; df=pd.read_csv(ROOT/'outputs/scored_calls.csv')
st.title('Scam Intelligence'); st.caption('Taxonomy, transcript cues, and behavioral indicators.'); st.metric('Known scam classes',df.loc[df.is_scam==1,'scam_type'].nunique()); st.bar_chart(df.loc[df.is_scam==1,'scam_type'].value_counts()); st.dataframe(df.sort_values('risk_score',ascending=False).head(50),use_container_width=True,hide_index=True)
