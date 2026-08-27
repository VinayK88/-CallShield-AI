from pathlib import Path
import argparse, json
from generate_data import generate_calls
from model import train_and_score
from model_lab import save_model_lab
from campaigns import rank_campaigns
from interventions import intervention

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def main(rows):
    OUT.mkdir(exist_ok=True)
    df = generate_calls(rows)

    _, scored, metrics = train_and_score(df)
    scored["intervention"] = [
        intervention(r.risk_score, int(r.prior_reports), int(r.spoof_signal))
        for r in scored.itertuples()
    ]

    campaigns = rank_campaigns(scored)
    scored.to_csv(OUT / "scored_calls.csv", index=False)
    campaigns.to_csv(OUT / "campaigns.csv", index=False)

    # Advanced ML lab: boosted nonlinear model + novelty detection + ensemble.
    _, model_comparison, _ = save_model_lab(df, OUT)
    champion = model_comparison.sort_values("pr_auc", ascending=False).iloc[0]

    kpis = {
        "blocked_rate": float((scored.intervention == "BLOCK").mean()),
        "screened_rate": float((scored.intervention == "CALL SCREEN").mean()),
        "high_risk_rate": float((scored.risk_score >= .90).mean()),
        "avg_reports": float(scored.prior_reports.mean()),
        "avg_reach": float(scored.unique_recipients_1h.mean()),
        "spoof_rate": float(scored.spoof_signal.mean()),
        "robotic_call_rate": float((scored.robotic_voice_score >= .60).mean()),
        "estimated_protected_users": int(scored.loc[scored.predicted_scam == 1, "receiver_id"].nunique()),
        "ml_champion": str(champion["model"]),
        "ml_champion_pr_auc": float(champion["pr_auc"]),
    }

    (OUT / "summary.json").write_text(json.dumps({
        "model_evaluation": metrics,
        "kpis": kpis
    }, indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=30000)
    main(ap.parse_args().rows)
