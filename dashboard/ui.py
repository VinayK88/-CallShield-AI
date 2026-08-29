import streamlit as st

APPLE_CSS = r'''
<style>
:root{--ink:#1d1d1f;--muted:#6e6e73;--soft:#f5f5f7;--line:#e8e8ed;--blue:#0071e3;--green:#248a3d;--red:#d70015}
html,body,[class*="css"]{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","SF Pro Display","Helvetica Neue",Helvetica,Arial,sans-serif;color:var(--ink)}
.stApp{background:linear-gradient(180deg,#fff 0%,#fff 70%,#fafafa 100%)}
.block-container{max-width:1460px;padding-top:1.25rem;padding-bottom:5rem}
[data-testid="stSidebar"]{background:rgba(245,245,247,.90);backdrop-filter:blur(24px);border-right:1px solid rgba(0,0,0,.055)}
[data-testid="stSidebarNav"] a{border-radius:12px;margin:.12rem .35rem;padding:.38rem .55rem}
[data-testid="stSidebarNav"] a:hover{background:rgba(255,255,255,.75)}
[data-testid="stMetric"]{background:rgba(245,245,247,.86);border:1px solid rgba(0,0,0,.035);border-radius:28px;padding:1.18rem 1.22rem;min-height:118px;box-shadow:0 12px 34px rgba(0,0,0,.032)}
[data-testid="stMetricLabel"]{font-size:.72rem;color:#6e6e73;font-weight:650;letter-spacing:.01em}
[data-testid="stMetricValue"]{font-size:1.95rem;color:#1d1d1f;font-weight:650;letter-spacing:-.045em}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:24px;overflow:hidden;box-shadow:0 10px 28px rgba(0,0,0,.022)}
[data-testid="stAlert"]{border-radius:20px;border:1px solid var(--line)}
.stButton>button,.stDownloadButton>button{border-radius:999px;border:0;background:#0071e3;color:white;font-weight:600;padding:.55rem 1rem}
hr{border-color:var(--line)!important;margin:2.8rem 0!important}
.apple-hero{text-align:center;max-width:1080px;margin:0 auto;padding:4.7rem 1.1rem 3.2rem}
.apple-eyebrow{color:#0071e3;font-size:.76rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin-bottom:1rem}
.apple-title{font-size:4.9rem;line-height:.97;font-weight:650;letter-spacing:-.07em;margin:0;color:#1d1d1f}
.apple-sub{font-size:1.28rem;line-height:1.5;color:#6e6e73;max-width:870px;margin:1.25rem auto 0;letter-spacing:-.012em}
.apple-pills{display:flex;flex-wrap:wrap;gap:.5rem;justify-content:center;margin-top:1.45rem}
.apple-pill{background:#f5f5f7;border:1px solid rgba(0,0,0,.035);border-radius:999px;padding:.46rem .8rem;font-size:.73rem;color:#424245}
.apple-health{background:#eff8f1;color:#248a3d;font-weight:650}
.apple-card{background:linear-gradient(145deg,#f5f5f7,#fbfbfd);border:1px solid rgba(0,0,0,.035);border-radius:34px;padding:2.4rem 2.7rem;box-shadow:0 20px 48px rgba(0,0,0,.032);margin:1rem 0 2.5rem}
.apple-card-title{font-size:2rem;line-height:1.1;font-weight:650;letter-spacing:-.045em;margin:.35rem 0 .45rem}
.apple-card-copy{color:#6e6e73;font-size:.96rem;line-height:1.55;margin:0}
.apple-kicker{font-size:.71rem;color:#86868b;text-transform:uppercase;letter-spacing:.11em;font-weight:700;margin:1.3rem 0 .7rem}
.apple-section{font-size:1.92rem;font-weight:650;letter-spacing:-.045em;color:#1d1d1f;margin-bottom:.22rem}
.apple-section-sub{font-size:.94rem;line-height:1.5;color:#86868b;margin-bottom:1.15rem}
.apple-stat-row{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:1rem 0 1.4rem}
.apple-stat{background:#f5f5f7;border-radius:24px;padding:1.25rem 1.35rem;border:1px solid rgba(0,0,0,.035)}
.apple-stat-label{font-size:.69rem;color:#86868b;text-transform:uppercase;letter-spacing:.08em;font-weight:700}
.apple-stat-value{font-size:1.7rem;font-weight:650;letter-spacing:-.04em;margin-top:.25rem}
@media(max-width:900px){.apple-title{font-size:3.3rem}.apple-sub{font-size:1.05rem}.apple-hero{padding-top:2.8rem}.apple-stat-row{grid-template-columns:1fr}}
</style>
'''

def apply_theme():
    st.markdown(APPLE_CSS, unsafe_allow_html=True)

def hero(eyebrow, title, subtitle, pills=()):
    pills_html=''.join(f'<span class="apple-pill">{p}</span>' for p in pills)
    st.markdown(f'''<div class="apple-hero"><div class="apple-eyebrow">{eyebrow}</div><div class="apple-title">{title}</div><div class="apple-sub">{subtitle}</div><div class="apple-pills">{pills_html}</div></div>''', unsafe_allow_html=True)

def section(title, subtitle=''):
    st.markdown(f'<div class="apple-section">{title}</div><div class="apple-section-sub">{subtitle}</div>', unsafe_allow_html=True)

def kicker(text):
    st.markdown(f'<div class="apple-kicker">{text}</div>', unsafe_allow_html=True)

def callout(eyebrow, title, copy):
    st.markdown(f'''<div class="apple-card"><div class="apple-eyebrow">{eyebrow}</div><div class="apple-card-title">{title}</div><p class="apple-card-copy">{copy}</p></div>''', unsafe_allow_html=True)
