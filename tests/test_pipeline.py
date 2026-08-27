import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from generate_data import generate_calls
from model import train_and_score
from campaigns import rank_campaigns
def test_pipeline():
 df=generate_calls(3000,seed=7); _,s,m=train_and_score(df,seed=7); assert 0<=m['false_positive_rate']<=.03; assert m['pr_auc']>.70; assert 'risk_score' in s; assert 'campaign_risk' in rank_campaigns(s)
