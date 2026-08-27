import numpy as np
def rank_campaigns(scored):
 a=scored.groupby("caller_id").agg(calls=("call_id","count"),recipients=("receiver_id","nunique"),avg_risk=("risk_score","mean"),reports=("prior_reports","sum"),repeat_similarity=("repeat_script_similarity","mean"),spoof_rate=("spoof_signal","mean"),scam_rate=("is_scam","mean")).reset_index(); a["campaign_risk"]=np.clip(.25*np.clip(a["recipients"]/30,0,1)+.25*a["avg_risk"]+.15*np.clip(a["reports"]/12,0,1)+.15*a["repeat_similarity"]+.10*a["spoof_rate"]+.10*a["scam_rate"],0,1); return a.sort_values("campaign_risk",ascending=False)
