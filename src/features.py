from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
NUMERIC=["calls_1h","unique_recipients_1h","duration_sec","prior_reports","new_number","spoof_signal","repeat_script_similarity","robotic_voice_score","urgency_score","credential_request","payment_request","hour"]
def make_preprocessor(): return ColumnTransformer([("text",TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=5000),"transcript"),("num",StandardScaler(),NUMERIC)])
