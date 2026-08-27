from __future__ import annotations
import numpy as np, pandas as pd
SCAM_TYPES=["legitimate","robocall","telemarketing","bank_impersonation","tech_support_scam","government_impersonation","ato_scam","investment_scam"]
TRANSCRIPTS={
"legitimate":["Hi, calling to confirm dinner plans for tonight.","Your appointment is confirmed for tomorrow at 10.","This is your delivery driver, I am outside."],
"robocall":["Press one now to receive your special offer.","This is an automated message about your account eligibility."],
"telemarketing":["We can lower your monthly bill today if you act now.","This exclusive plan is available only during this call."],
"bank_impersonation":["We detected suspicious activity. Please verify your banking PIN.","Your bank account is locked. Read the one time code to me."],
"tech_support_scam":["Your computer has a virus. Install remote support software now.","Please download this remote access tool so I can fix the issue."],
"government_impersonation":["This is the tax authority. Pay immediately to avoid arrest.","A warrant has been issued unless you resolve this balance today."],
"ato_scam":["Your account recovery request is pending. Read me the verification code.","Approve the MFA prompt now so I can secure your account."],
"investment_scam":["Guaranteed crypto returns if you transfer funds today.","This investment opportunity can double your money this week."]}
def generate_calls(n=30000,seed=42):
 r=np.random.default_rng(seed); probs=np.array([.73,.06,.05,.04,.035,.025,.03,.03]); labels=r.choice(SCAM_TYPES,n,p=probs/probs.sum())
 callers=[f"caller_{i:05d}" for i in range(max(500,n//20))]; receivers=[f"user_{i:06d}" for i in range(max(4000,n//4))]; rows=[]
 for i,l in enumerate(labels):
  scam=l!="legitimate"; rows.append({"call_id":f"call_{i:07d}","caller_id":r.choice(callers),"receiver_id":r.choice(receivers),"scam_type":l,"is_scam":int(scam),"calls_1h":int(r.poisson(28 if scam else 3)),"unique_recipients_1h":int(r.poisson(18 if scam else 2)+1),"duration_sec":round(max(3,r.normal(52 if scam else 95,35)),1),"prior_reports":int(r.poisson(1.8 if scam else .04)),"new_number":int(r.random()<(.48 if scam else .08)),"spoof_signal":int(r.random()<(.42 if scam else .015)),"repeat_script_similarity":round(float(np.clip(r.normal(.83 if scam else .21,.12),0,1)),3),"robotic_voice_score":round(float(np.clip(r.normal(.70 if l=="robocall" else (.38 if scam else .12),.15),0,1)),3),"urgency_score":round(float(np.clip(r.normal(.78 if scam else .14,.16),0,1)),3),"credential_request":int(l in {"bank_impersonation","ato_scam"} and r.random()<.88),"payment_request":int(l in {"government_impersonation","investment_scam","tech_support_scam"} and r.random()<.76),"hour":int(r.integers(0,24)),"transcript":r.choice(TRANSCRIPTS[l])})
 return pd.DataFrame(rows)
