# helpers.py — Shared utilities, CSS, and chart helpers
# PredictiveBI — Predictive Analytics for Software Project Success

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# ── BRAND ─────────────────────────────────────────────────────────────────────
APP_NAME    = "PredictiveBI"
APP_TITLE   = "Predictive Analytics for Software Project Success"
APP_SUB     = "A Business Intelligence Approach"
APP_ORG     = "University of West London"
APP_LABEL   = "Research Prototype"

# ── COLOURS ───────────────────────────────────────────────────────────────────
C = dict(
    navy="#1F3864", blue="#2563EB", mid="#3B82F6", light="#DBEAFE",
    green="#059669", green2="#34D399", amber="#D97706", amber2="#FCD34D",
    red="#DC2626",  red2="#F87171", purple="#7C3AED", purple2="#A78BFA",
    grey="#F1F5F9", white="#FFFFFF", text="#1E293B", text2="#64748B",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif!important}
.main .block-container{padding:1rem 1.6rem;max-width:1240px}
/* Sidebar */
section[data-testid="stSidebar"]{background:linear-gradient(175deg,#0f1d35,#1a2f4e)!important;border-right:1px solid #1e3a5f}
section[data-testid="stSidebar"] *{color:#c8daea!important}
/* KPI card */
.kpi{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:16px 18px;
     text-align:center;position:relative;overflow:hidden;
     box-shadow:0 1px 8px rgba(0,0,0,.06);transition:transform .2s,box-shadow .2s}
.kpi:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.1)}
.kpi::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:14px 14px 0 0}
.kpi.b::before{background:linear-gradient(90deg,#2563EB,#06B6D4)}
.kpi.g::before{background:linear-gradient(90deg,#059669,#34D399)}
.kpi.a::before{background:linear-gradient(90deg,#D97706,#FCD34D)}
.kpi.r::before{background:linear-gradient(90deg,#DC2626,#F87171)}
.kpi.p::before{background:linear-gradient(90deg,#7C3AED,#A78BFA)}
.kpi.c::before{background:linear-gradient(90deg,#0891B2,#67E8F9)}
.kv{font-size:10px;font-weight:700;color:#94A3B8;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px}
.kn{font-size:26px;font-weight:800;color:#1E293B;font-family:'JetBrains Mono',monospace;line-height:1.1}
.ks{font-size:11px;color:#64748B;margin-top:3px}
/* Insight boxes */
.ins{border-radius:10px;padding:12px 16px;margin-bottom:14px;
     font-size:13.5px;line-height:1.65;border-left:4px solid}
.ii{background:#EFF6FF;border-color:#3B82F6;color:#1E3A5F}
.iw{background:#FFFBEB;border-color:#F59E0B;color:#78350F}
.id{background:#FEF2F2;border-color:#EF4444;color:#7F1D1D}
.is{background:#F0FDF4;border-color:#10B981;color:#064E3B}
.ip{background:#F5F3FF;border-color:#8B5CF6;color:#4C1D95}
/* Section head */
.sh{font-size:14px;font-weight:700;color:#1E3A5F;padding:7px 0 5px;
    border-bottom:2px solid #E2E8F0;margin-bottom:14px;display:flex;align-items:center;gap:6px}
/* RQ banner */
.rq{background:linear-gradient(135deg,#EFF6FF,#F0FDF4);border:1px solid #BFDBFE;
    border-radius:9px;padding:9px 15px;font-size:13px;color:#1E40AF;
    margin-bottom:16px;font-weight:500}
/* Interview card */
.icard{background:#fff;border:1px solid #E2E8F0;border-radius:12px;
       padding:16px 18px;margin-bottom:10px;
       box-shadow:0 1px 6px rgba(0,0,0,.05)}
/* Quote box */
.qbox{background:#F8FAFC;border-left:4px solid #3B82F6;border-radius:0 8px 8px 0;
      padding:10px 14px;margin:8px 0;font-size:13px;color:#334155;font-style:italic}
/* Badge */
.badge{display:inline-block;padding:2px 10px;border-radius:20px;
       font-size:10px;font-weight:700;letter-spacing:.5px}
.badge-g{background:#D1FAE5;color:#065F46;border:1px solid #6EE7B7}
.badge-b{background:#DBEAFE;color:#1E40AF;border:1px solid #93C5FD}
.badge-a{background:#FEF3C7;color:#92400E;border:1px solid #FCD34D}
.badge-r{background:#FEE2E2;color:#7F1D1D;border:1px solid #F87171}
.badge-p{background:#EDE9FE;color:#4C1D95;border:1px solid #A78BFA}
/* Upload box */
.upload-info{background:#F0FDF4;border:1px solid #BBF7D0;border-radius:10px;
             padding:10px 14px;font-size:13px;color:#065F46;margin-bottom:12px}
.default-info{background:#EFF6FF;border:1px solid #BFDBFE;border-radius:10px;
              padding:10px 14px;font-size:13px;color:#1E40AF;margin-bottom:12px}
/* Rec card */
.rcard{background:#fff;border:1px solid #E2E8F0;border-radius:12px;
       padding:15px 17px;margin-bottom:10px}
/* Header bar */
.hbar{background:linear-gradient(135deg,#1F3864,#2563EB);
      border-radius:12px;padding:16px 22px;margin-bottom:18px;color:#fff}
.hbar h2{font-size:20px;font-weight:800;margin:0 0 2px}
.hbar p{font-size:12px;opacity:.85;margin:0}
/* Footer */
.footer{text-align:center;padding:18px 0 6px;border-top:1px solid #E2E8F0;
        color:#94A3B8;font-size:11.5px;margin-top:28px}
/* Download btn */
.stDownloadButton>button{
    background:linear-gradient(135deg,#1F3864,#2563EB)!important;
    color:#fff!important;border:none!important;border-radius:8px!important;
    font-weight:700!important;font-size:13px!important;padding:8px 20px!important}
/* Scrollbar */
::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:#F1F5F9}
::-webkit-scrollbar-thumb{background:#CBD5E1;border-radius:3px}
/* Real data tag */
.rtag{background:#D1FAE5;color:#065F46;border:1px solid #6EE7B7;
      border-radius:20px;padding:2px 10px;font-size:10px;font-weight:700;
      display:inline-block;margin-left:6px}
</style>"""

# ── CHART THEME ───────────────────────────────────────────────────────────────
THEME = dict(
    plot_bgcolor="white", paper_bgcolor="white",
    font=dict(family="Inter", color="#334155", size=12),
    margin=dict(l=12, r=12, t=36, b=12),
)

def tidy(fig):
    fig.update_xaxes(showgrid=False, linecolor="#E2E8F0", tickfont_size=11)
    fig.update_yaxes(gridcolor="#F1F5F9", linecolor="#E2E8F0", tickfont_size=11)
    fig.update_layout(**THEME)
    return fig

# ── HTML HELPERS ──────────────────────────────────────────────────────────────
def kpi(label, value, sub, cls):
    return f'<div class="kpi {cls}"><div class="kv">{label}</div><div class="kn">{value}</div><div class="ks">{sub}</div></div>'

def ins(msg, t="i"):
    return f'<div class="ins i{t}">{msg}</div>'

def sh(title):
    st.markdown(f'<div class="sh">{title}</div>', unsafe_allow_html=True)

def rq(text):
    st.markdown(f'<div class="rq">🎓 <strong>Research Link:</strong> {text}</div>', unsafe_allow_html=True)

def header(title, subtitle=""):
    st.markdown(f"""
    <div class="hbar">
        <h2>{title}</h2>
        <p>{subtitle}</p>
    </div>""", unsafe_allow_html=True)

def badge(text, cls="b"):
    return f'<span class="badge badge-{cls}">{text}</span>'

def quote_box(text):
    return f'<div class="qbox">"{text}"</div>'

def rtag():
    return '<span class="rtag">✓ REAL DATA n=92</span>'

def footer():
    st.markdown(f"""
    <div class="footer">
        <strong>{APP_NAME}</strong> &nbsp;·&nbsp; {APP_TITLE} &nbsp;·&nbsp; {APP_SUB}<br>
        {APP_ORG} &nbsp;·&nbsp; {APP_LABEL} &nbsp;·&nbsp; Real Survey Data n=92
    </div>""", unsafe_allow_html=True)

# ── RISK SCORER ───────────────────────────────────────────────────────────────
def score_risk(vel, defs, exp, req, dep, sat):
    s = (100-vel)*0.30 + defs*0.40 + req*0.30 - exp*0.5 - sat*0.8 - dep*0.15
    if   s > 28: lbl, conf = "High",   min(0.95, 0.55+(s-28)*0.012)
    elif s > 14: lbl, conf = "Medium", min(0.90, 0.50+(s-14)*0.015)
    else:        lbl, conf = "Low",    min(0.95, 0.55+(14-s)*0.012)
    score = min(100, max(0, round(s+30)))
    return lbl, conf, score

# ── ADOPTION READINESS ────────────────────────────────────────────────────────
def adoption_readiness(trust, data_quality, leadership, training):
    score = trust*0.35 + data_quality*0.25 + leadership*0.25 + training*0.15
    if   score >= 71: label, color = "High Readiness",     "#059669"
    elif score >= 41: label, color = "Moderate Readiness", "#D97706"
    else:             label, color = "Low Readiness",       "#DC2626"
    return round(score), label, color

# ── BI MATURITY ───────────────────────────────────────────────────────────────
def bi_maturity(dash_use, analytics_use, data_quality, governance):
    score = dash_use*0.30 + analytics_use*0.25 + data_quality*0.25 + governance*0.20
    if   score >= 75: label, level = "Advanced",    5
    elif score >= 50: label, level = "Developing",  3
    else:             label, level = "Basic",        1
    return round(score), label, level
