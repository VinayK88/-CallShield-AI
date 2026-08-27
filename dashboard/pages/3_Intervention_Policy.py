from pathlib import Path
import pandas as pd, streamlit as st
ROOT=Path(__file__).resolve().parents[2]; df=pd.read_csv(ROOT/'outputs/scored_calls.csv')
st.title('Intervention Policy'); st.caption('Translate risk into proportional user protection.'); st.code('ALLOW → LABEL SUSPECTED SPAM → CALL SCREEN → SILENCE → BLOCK'); st.bar_chart(df['intervention'].value_counts()); st.dataframe(df.sort_values('risk_score',ascending=False)[['caller_id','risk_score','prior_reports','spoof_signal','intervention','transcript']].head(40),use_container_width=True,hide_index=True)
