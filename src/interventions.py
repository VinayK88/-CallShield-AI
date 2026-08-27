def intervention(score,reports,spoof):
 if score>=.92 or (score>=.85 and reports>=3): return "BLOCK"
 if score>=.82: return "SILENCE"
 if score>=.70 or (spoof and score>=.55): return "CALL SCREEN"
 if score>=.52: return "LABEL SUSPECTED SPAM"
 return "ALLOW"
