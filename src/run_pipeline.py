from pathlib import Path
import argparse,json
from generate_data import generate_calls
from model import train_and_score
from campaigns import rank_campaigns
from interventions import intervention
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"outputs"
def main(rows):
 OUT.mkdir(exist_ok=True); df=generate_calls(rows); _,s,m=train_and_score(df); s["intervention"]=[intervention(r.risk_score,int(r.prior_reports),int(r.spoof_signal)) for r in s.itertuples()]; c=rank_campaigns(s); s.to_csv(OUT/"scored_calls.csv",index=False); c.to_csv(OUT/"campaigns.csv",index=False); k={"blocked_rate":float((s.intervention=="BLOCK").mean()),"screened_rate":float((s.intervention=="CALL SCREEN").mean()),"high_risk_rate":float((s.risk_score>=.90).mean()),"avg_reports":float(s.prior_reports.mean()),"avg_reach":float(s.unique_recipients_1h.mean()),"spoof_rate":float(s.spoof_signal.mean()),"robotic_call_rate":float((s.robotic_voice_score>=.60).mean()),"estimated_protected_users":int(s.loc[s.predicted_scam==1,"receiver_id"].nunique())}; (OUT/"summary.json").write_text(json.dumps({"model_evaluation":m,"kpis":k},indent=2))
if __name__=="__main__":
 ap=argparse.ArgumentParser(); ap.add_argument("--rows",type=int,default=30000); main(ap.parse_args().rows)
