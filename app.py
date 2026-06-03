# app.py — PredictiveBI  |  MSc Research Prototype
# Predictive Analytics for Software Project Success
# University of West London  |  Real Survey Data n=92

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="PredictiveBI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from helpers import (CSS, THEME, tidy, kpi, ins, sh, rq, header,
                     badge, quote_box, rtag, footer,
                     score_risk, adoption_readiness, bi_maturity,
                     APP_NAME, APP_TITLE, APP_SUB, APP_ORG, APP_LABEL,
                     C)
from loader  import load_survey
from report_gen import generate_full_report, to_csv

st.markdown(CSS, unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:8px 4px 16px;border-bottom:1px solid #1e3a5f;margin-bottom:10px">
      <div style="font-size:22px;font-weight:800;color:#60a5fa;letter-spacing:-0.5px">
        📊 {APP_NAME}</div>
      <div style="font-size:11px;color:#5b8db0;margin-top:3px">{APP_TITLE}</div>
      <div style="font-size:10px;color:#3d6a8a;margin-top:1px">{APP_ORG}</div>
      <div style="margin-top:6px;background:#1e3a5f;border-radius:6px;
                  padding:3px 9px;font-size:10px;color:#34d399;font-weight:700;
                  display:inline-block">✓ {APP_LABEL}</div>
    </div>""", unsafe_allow_html=True)

    # ── File upload ────────────────────────────────────────────────────────────
    st.markdown('<div style="font-size:11px;color:#6fa0c0;font-weight:700;'
                'letter-spacing:.5px;margin-bottom:6px">DATASET</div>',
                unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload your own dataset",
                                type=["xlsx","csv"],
                                label_visibility="collapsed",
                                help="Upload .xlsx or .csv to analyse your own data")

    # ── Navigation ─────────────────────────────────────────────────────────────
    st.markdown('<div style="font-size:11px;color:#6fa0c0;font-weight:700;'
                'letter-spacing:.5px;margin:12px 0 6px">NAVIGATION</div>',
                unsafe_allow_html=True)
    page = st.radio("", [
        "🏠  Executive Dashboard",
        "👥  Respondent Profile",
        "📊  Survey Results",
        "🔮  Predictive Analytics",
        "🧠  Explainable AI",
        "⚡  Agile & DevOps",
        "🛡️  Ethical Governance",
        "📉  Adoption Gap",
        "🎯  Project Risk Analysis",
        "📈  Adoption Readiness",
        "🏗️  BI Maturity",
        "💬  Interview Findings",
        "💡  Recommendations",
        "🚀  Future Roadmap",
        "📄  Generate Report",
    ], label_visibility="collapsed")

    st.markdown("""
    <hr style="border-color:#1e3358;margin:12px 0">
    <div style="font-size:10px;color:#4a7a9b;line-height:1.9">
      <b style="color:#6fa0c0">Data:</b> Real survey n=92<br>
      <b style="color:#6fa0c0">Type:</b> Primary + Secondary<br>
      <b style="color:#6fa0c0">Org:</b> University of West London
    </div>""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_default():
    return load_survey(None)

if uploaded:
    sd = load_survey(uploaded)
    st.markdown(f'<div class="upload-info">📂 <strong>Uploaded dataset active:</strong> '
                f'{uploaded.name} — n={sd.n} respondents. '
                f'All charts updated automatically.</div>', unsafe_allow_html=True)
else:
    sd = load_default()
    st.markdown(f'<div class="default-info">📋 <strong>Currently analysing dissertation survey dataset (n = 92).</strong> '
                f'You can upload your own .xlsx or .csv file in the sidebar to analyse a different dataset.</div>',
                unsafe_allow_html=True)

# ── CHART HELPERS ─────────────────────────────────────────────────────────────
RISK_COL = {"High":"#DC2626","Medium":"#D97706","Low":"#059669"}
RISK_BG  = {"High":"#FEF2F2","Medium":"#FFFBEB","Low":"#F0FDF4"}


def prog_bar(label, pct, color="#2563EB"):
    return f"""
    <div style="margin-bottom:10px">
      <div style="display:flex;justify-content:space-between;margin-bottom:4px;font-size:12.5px">
        <span style="color:#334155;font-weight:500">{label}</span>
        <span style="color:#1E293B;font-weight:700;font-family:'JetBrains Mono',monospace">{pct}%</span>
      </div>
      <div style="height:7px;background:#F1F5F9;border-radius:4px;overflow:hidden">
        <div style="width:{pct}%;height:100%;background:{color};border-radius:4px;
                    transition:width 1s ease"></div>
      </div>
    </div>"""


# ══════════════════════════════════════════════════════════════════════════════
# P1 — EXECUTIVE DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if "Executive" in page:
    header(f"Executive Dashboard {rtag()}",
           "BI-driven project intelligence — real survey data")
    rq("RQ1 & RQ3 — How do BI dashboards improve project visibility and decision-making?")

    c = st.columns(5)
    c[0].markdown(kpi("BI Mean",       f"{sd.bi_mean}",  "/ 5.0  Composite","b"),  unsafe_allow_html=True)
    c[1].markdown(kpi("PA Mean",       f"{sd.pa_mean}",  "/ 5.0  Composite","g"),  unsafe_allow_html=True)
    c[2].markdown(kpi("Trust Mean",    f"{sd.tr_mean}",  "/ 5.0  Composite","p"),  unsafe_allow_html=True)
    c[3].markdown(kpi("Privacy Conc.", f"{sd.privacy_pct}%","Q21 agree","r"),       unsafe_allow_html=True)
    c[4].markdown(kpi("Rarely Use",    f"{sd.rarely_never_pct}%","adoption gap","a"),unsafe_allow_html=True)

    st.markdown(ins(
        f"<strong>Key Finding (n={sd.n}):</strong> BI composite mean <strong>{sd.bi_mean}</strong>/5.0 · "
        f"PA composite mean <strong>{sd.pa_mean}</strong>/5.0 · "
        f"Trust-Adoption: <strong>r = {sd.corr['trust_pa']}</strong> (strongest correlation) · "
        f"<strong>{sd.rarely_never_pct}%</strong> rarely/never use tools — adoption gap confirmed.","i"),
        unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        sh("📊 Composite Scale Means — Real Survey Data")
        sections = {
            "BI Tools\n(Q6-10)": sd.bi_mean,
            "PA Usage\n(Q11-15)": sd.pa_mean,
            "Trust/Ease\n(Q16-19)": sd.tr_mean,
            "Success\n(Q22-25)": sd.suc_mean,
            "Ethics\n(Q20-21)": sd.eth_mean,
        }
        fig = go.Figure(go.Bar(
            x=list(sections.keys()), y=list(sections.values()),
            marker_color=[C["blue"],C["purple"],C["green"],C["amber"],C["red"]],
            text=[f"{v:.3f}" for v in sections.values()],
            textposition="outside"
        ))
        fig.add_hline(y=4.0, line_dash="dot", line_color=C["amber"], annotation_text="4.0")
        fig.update_layout(title=f"Composite Means (n={sd.n})", yaxis_range=[3.3,4.5], bargap=0.35)
        st.plotly_chart(tidy(fig), use_container_width=True)

    with col2:
        sh("🔗 Pearson Correlations")
        cdf = pd.DataFrame({
            "Pair":["BI->Success","PA->Success","Trust->Success","Trust->PA (★)"],
            "r":   [sd.corr["bi_success"],sd.corr["pa_success"],
                    sd.corr["trust_success"],sd.corr["trust_pa"]],
        })
        fig2 = px.bar(cdf, x="r", y="Pair", orientation="h",
            color="r", color_continuous_scale=["#DBEAFE","#2563EB","#1E3864"],
            text="r")
        fig2.update_traces(texttemplate="r = %{text:.3f}", textposition="outside")
        fig2.add_vline(x=0.5, line_dash="dot", line_color=C["amber"])
        fig2.update_layout(title="Correlations (Real Data)", coloraxis_showscale=False,
                           xaxis_range=[0,0.82])
        st.plotly_chart(tidy(fig2), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        sh("📊 Cronbach Alpha — Scale Reliability")
        adf = pd.DataFrame({
            "Scale":["BI (Q6-10)","PA (Q11-15)","Trust (Q16-19)","Success (Q22-25)"],
            "Alpha":[sd.cronbach["bi"],sd.cronbach["pa"],
                     sd.cronbach["trust"],sd.cronbach["success"]],
        })
        fig3 = go.Figure(go.Bar(
            x=adf["Scale"], y=adf["Alpha"],
            marker_color=["#059669" if v>=0.70 else "#DC2626" for v in adf["Alpha"]],
            text=[f"a={v:.3f}" for v in adf["Alpha"]], textposition="outside"
        ))
        fig3.add_hline(y=0.70, line_dash="dot", line_color=C["amber"],
                       annotation_text="a=0.70 threshold")
        fig3.update_layout(title="Reliability (Cronbach Alpha)", yaxis_range=[0,1.0], bargap=0.35)
        st.plotly_chart(tidy(fig3), use_container_width=True)

    with col4:
        sh("🔄 Tool Usage Frequency (Q26)")
        fdf = pd.DataFrame({"Freq":list(sd.freq.keys()),"n":list(sd.freq.values())})
        fdf["Pct"] = (fdf["n"]/sd.n*100).round(1)
        fig4 = px.pie(fdf, values="n", names="Freq",
            color="Freq",
            color_discrete_map={"Very Frequently":C["green"],"Frequently":C["blue"],
                                 "Occasionally":C["amber"],"Rarely":C["red"],"Never":"#7F1D1D"},
            hole=0.52)
        fig4.update_traces(textposition="outside", textinfo="percent+label")
        fig4.update_layout(title=f"Q26 Usage Frequency (n={sd.n})",
                           legend=dict(orientation="h",y=-0.15))
        st.plotly_chart(tidy(fig4), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# P2 — RESPONDENT PROFILE
# ══════════════════════════════════════════════════════════════════════════════
elif "Respondent" in page:
    header(f"Respondent Profile {rtag()}", f"Real demographics — n={sd.n} respondents")
    rq("Chapter 4.2 — Sample Profile and Demographic Implications")

    col1,col2 = st.columns(2)
    with col1:
        sh("👤 Job Roles (Q1)")
        rdf2 = pd.DataFrame({"Role":list(sd.roles.keys()),"n":list(sd.roles.values())})
        rdf2["Pct"] = (rdf2["n"]/sd.n*100).round(1)
        rdf2 = rdf2.sort_values("n",ascending=True)
        fig = px.bar(rdf2, x="n", y="Role", orientation="h",
            color="n", color_continuous_scale=["#DBEAFE","#2563EB","#1E3864"],
            text=rdf2.Pct.apply(lambda v:f"{v}%"))
        fig.update_traces(textposition="outside")
        fig.update_layout(title=f"Respondent Roles (n={sd.n})", coloraxis_showscale=False)
        st.plotly_chart(tidy(fig), use_container_width=True)

    with col2:
        sh("📅 Experience (Q2)")
        edf = pd.DataFrame({"Exp":list(sd.exp.keys()),"n":list(sd.exp.values())})
        fig2 = px.pie(edf, values="n", names="Exp",
            color_discrete_sequence=[C["red"],C["amber"],C["blue"],C["green"],C["purple"]],
            hole=0.50)
        fig2.update_traces(textposition="outside", textinfo="percent+label")
        fig2.update_layout(title="Years of Experience", legend=dict(orientation="h",y=-0.15))
        st.plotly_chart(tidy(fig2), use_container_width=True)

    col3,col4 = st.columns(2)
    with col3:
        sh("⚙️ Methodology (Q3)")
        mdf = pd.DataFrame({"Method":list(sd.method.keys()),"n":list(sd.method.values())})
        mdf["Pct"] = (mdf["n"]/sd.n*100).round(1)
        mdf = mdf.sort_values("n",ascending=False).head(8)
        fig3 = px.bar(mdf, x="Method", y="n",
            color="n", color_continuous_scale=["#DBEAFE","#1E3864"],
            text=mdf.Pct.apply(lambda v:f"{v}%"))
        fig3.update_traces(textposition="outside")
        fig3.update_layout(title="Development Methodology", coloraxis_showscale=False, bargap=0.3)
        st.plotly_chart(tidy(fig3), use_container_width=True)

    with col4:
        sh("🏢 Organisation Size (Q4)")
        odf = pd.DataFrame({"Size":list(sd.org.keys()),"n":list(sd.org.values())})
        odf["Pct"] = (odf["n"]/sd.n*100).round(1)
        fig4 = px.bar(odf, x="Size", y="n",
            color="n", color_continuous_scale=["#DBEAFE","#1E3864"],
            text=odf.Pct.apply(lambda v:f"{v}%"))
        fig4.update_traces(textposition="outside")
        fig4.update_layout(title="Organisation Size", coloraxis_showscale=False, bargap=0.4)
        st.plotly_chart(tidy(fig4), use_container_width=True)

    sh("🌍 Industry Sector (Q5)")
    sdf2 = pd.DataFrame({"Sector":list(sd.sector.keys()),"n":list(sd.sector.values())})
    sdf2["Pct"] = (sdf2["n"]/sd.n*100).round(1)
    sdf2 = sdf2.sort_values("n",ascending=True)
    fig5 = px.bar(sdf2, x="n", y="Sector", orientation="h",
        color="n", color_continuous_scale=["#DBEAFE","#2563EB","#1E3864"],
        text=sdf2.Pct.apply(lambda v:f"{v}%"))
    fig5.update_traces(textposition="outside")
    fig5.update_layout(title="Industry Sector Distribution", coloraxis_showscale=False)
    st.plotly_chart(tidy(fig5), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# P3 — SURVEY RESULTS
# ══════════════════════════════════════════════════════════════════════════════
elif "Survey Results" in page:
    header(f"Survey Results {rtag()}", f"All Q6-Q25 Likert results — n={sd.n}")
    rq("Chapter 4.3-4.6 — Full Likert Scale Analysis")

    tab1,tab2,tab3,tab4,tab5 = st.tabs([
        "🔷 BI Tools (Q6-10)","🔶 PA Usage (Q11-15)",
        "🟢 Trust/Ease (Q16-19)","🔴 Ethics (Q20-21)","🟣 Success (Q22-25)"])

    def section_tab(qs_keys, title, color):
        qs = {k:sd.q_stats[k] for k in qs_keys if k in sd.q_stats}
        means  = [qs[k]["mean"]  for k in qs]
        agrees = [qs[k]["agree"] for k in qs]
        labels = [f"{k}: {qs[k]['label'][:38]}..." if len(qs[k]['label'])>38
                  else f"{k}: {qs[k]['label']}" for k in qs]
        col1,col2 = st.columns(2)
        with col1:
            fig = px.bar(x=means, y=labels, orientation="h",
                color=means, color_continuous_scale=["#DBEAFE",color,"#1E3864"],
                text=[f"{v:.3f}" for v in means])
            fig.update_traces(textposition="outside")
            fig.update_layout(title=f"Mean Scores — {title}",
                              coloraxis_showscale=False, xaxis_range=[2.5,5.0])
            st.plotly_chart(tidy(fig), use_container_width=True)
        with col2:
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(name="Agree%",    x=list(qs.keys()),
                y=[qs[k]["agree"]   for k in qs], marker_color=color))
            fig2.add_trace(go.Bar(name="Neutral%",  x=list(qs.keys()),
                y=[qs[k]["neutral"] for k in qs], marker_color="#94A3B8"))
            fig2.add_trace(go.Bar(name="Disagree%", x=list(qs.keys()),
                y=[qs[k]["disagree"]for k in qs], marker_color=C["red"]))
            fig2.update_layout(barmode="stack", title="Response Distribution",
                               legend=dict(orientation="h",y=1.1))
            fig2.update_yaxes(ticksuffix="%")
            st.plotly_chart(tidy(fig2), use_container_width=True)

        tbl = pd.DataFrame({
            "Q":      list(qs.keys()),
            "Statement": [qs[k]["label"] for k in qs],
            "Mean":   [qs[k]["mean"]    for k in qs],
            "Agree%": [qs[k]["agree"]   for k in qs],
            "Neutral%":[qs[k]["neutral"] for k in qs],
            "Disagree%":[qs[k]["disagree"]for k in qs],
            "n":      [qs[k]["n"]       for k in qs],
        })
        st.dataframe(tbl, use_container_width=True, hide_index=True)

    with tab1:
        st.markdown(ins(f"BI composite mean: <strong>{sd.bi_mean}</strong>/5.0 | "
                        f"Cronbach a={sd.cronbach['bi']} | "
                        f"Q8 risk identification: highest rated ({sd.q_stats['Q8']['mean']:.3f})","i"),
                    unsafe_allow_html=True)
        section_tab(["Q6","Q7","Q8","Q9","Q10"],"BI Tool Usage",C["blue"])
    with tab2:
        st.markdown(ins(f"PA composite mean: <strong>{sd.pa_mean}</strong>/5.0 | "
                        f"Cronbach a={sd.cronbach['pa']} | "
                        f"Maturity gap vs BI: {round(sd.bi_mean-sd.pa_mean,3)}","w"),
                    unsafe_allow_html=True)
        section_tab(["Q11","Q12","Q13","Q14","Q15"],"PA Usage",C["purple"])
    with tab3:
        st.markdown(ins(f"Trust mean: <strong>{sd.tr_mean}</strong>/5.0 | "
                        f"Cronbach a={sd.cronbach['trust']} | "
                        f"Q19 training: highest ({sd.q_stats['Q19']['mean']:.3f}) | "
                        f"Q17 transparency gap: {sd.q_stats['Q17']['mean']:.3f}","i"),
                    unsafe_allow_html=True)
        section_tab(["Q16","Q17","Q18","Q19"],"Trust & Ease",C["green"])
    with tab4:
        st.markdown(ins(f"<strong>Mainstream anxiety:</strong> Q21 privacy {sd.privacy_pct}% agree · "
                        f"Q20 bias {sd.bias_pct}% agree — structural governance required.","d"),
                    unsafe_allow_html=True)
        section_tab(["Q20","Q21"],"Ethical Concerns",C["red"])
    with tab5:
        st.markdown(ins(f"Success mean: <strong>{sd.suc_mean}</strong>/5.0 | "
                        f"Cronbach a={sd.cronbach['success']} — below 0.70, "
                        f"interpreted as evidence of project success multidimensionality.","w"),
                    unsafe_allow_html=True)
        section_tab(["Q22","Q23","Q24","Q25"],"Project Success",C["amber"])


# ══════════════════════════════════════════════════════════════════════════════
# P4 — PREDICTIVE ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif "Predictive" in page:
    header("🔮 Predictive Analytics Module", "ML-based project risk prediction")
    rq(f"RQ2 & RQ5 — PA usage -> success r={sd.corr['pa_success']} (real n={sd.n})")

    col_in, col_out = st.columns([1,1.7])
    with col_in:
        sh("🎛️ Project Input Parameters")
        sv  = st.slider("Sprint Velocity",         20, 100, 62)
        dc  = st.slider("Defect Count",             0,  50, 14)
        te  = st.slider("Team Experience (yrs)",    1,  10,  5)
        rc  = st.slider("Requirement Changes",       0,  20,  5)
        dep = st.slider("Deploy Frequency/sprint",  1,  30, 10)
        ts  = st.slider("Team Satisfaction (1-5)",  1.0, 5.0, 3.8, 0.1)

        rl, rp, rs = score_risk(sv, dc, te, rc, dep, ts)
        col = RISK_COL[rl]; bg = RISK_BG[rl]
        st.markdown(f"""
        <div style="background:{bg};border:2px solid {col};border-radius:14px;
                    padding:18px;text-align:center;margin-top:14px">
          <div style="font-size:10px;font-weight:700;color:#64748B;letter-spacing:.8px;
                      text-transform:uppercase;margin-bottom:4px">Risk Prediction</div>
          <div style="font-size:34px;font-weight:800;color:{col};
                      font-family:'JetBrains Mono',monospace">{rl} Risk</div>
          <div style="font-size:13px;color:#64748B;margin-top:4px">
            Confidence: <strong>{rp:.1%}</strong></div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:12px;padding:12px;background:#F8FAFC;border:1px solid #E2E8F0;
                    border-radius:10px;font-size:12px;color:#475569">
          <strong>Survey Benchmarks (n={sd.n}):</strong><br>
          PA-Success r = {sd.corr['pa_success']} &nbsp;|&nbsp;
          BI-Success r = {sd.corr['bi_success']}<br>
          Model accuracy: 87.8% (Setiawan, 2025) &nbsp;|&nbsp;
          Neural net: 93% (White Rose, 2025)
        </div>""", unsafe_allow_html=True)

    with col_out:
        sh("📊 Risk Probability Distribution")
        s = (100-sv)*0.30+dc*0.40+rc*0.30-te*0.5-ts*0.8-dep*0.15
        raw={"High":max(0,s-14)/40,"Medium":max(0,30-abs(s-21))/30,"Low":max(0,14-s)/30}
        tot=sum(raw.values()) or 1
        probs={k:v/tot for k,v in raw.items()}
        fig_p=go.Figure(go.Bar(
            x=[f"{k} Risk" for k in probs], y=list(probs.values()),
            marker_color=["#DC2626","#D97706","#059669"],
            text=[f"{v:.1%}" for v in probs.values()], textposition="outside"))
        fig_p.update_layout(title="Risk Class Probabilities",
                            yaxis_tickformat=".0%", bargap=0.35)
        st.plotly_chart(tidy(fig_p), use_container_width=True)

        sh("📈 Delivery Forecast (Next 8 Sprints)")
        base=75+sv*0.15-dc*0.3+dep*0.4
        fc=[min(99,max(20,base+i*0.6+np.random.default_rng(i).normal(0,1.5)))
            for i in range(1,9)]
        fig_fc=go.Figure()
        fig_fc.add_trace(go.Scatter(x=list(range(1,9)),y=fc,mode="lines+markers",
            line=dict(color=C["blue"],width=2.5),marker=dict(size=7),
            fill="tozeroy",fillcolor="rgba(37,99,235,.07)"))
        fig_fc.add_hline(y=80,line_dash="dot",line_color=C["amber"],annotation_text="Target 80%")
        fig_fc.update_layout(title="Simulated Delivery Forecast",yaxis_title="Success %")
        st.plotly_chart(tidy(fig_fc), use_container_width=True)

    kinds={"High":"d","Medium":"w","Low":"s"}
    msgs={"High":f"<strong>High Risk ({rp:.0%}):</strong> Defect count and velocity are primary drivers.",
          "Medium":f"<strong>Medium Risk ({rp:.0%}):</strong> Monitor requirement changes and workload.",
          "Low":f"<strong>Low Risk ({rp:.0%}):</strong> Metrics are healthy. Maintain current cadence."}
    st.markdown(ins(msgs[rl],kinds[rl]), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# P5 — EXPLAINABLE AI
# ══════════════════════════════════════════════════════════════════════════════
elif "Explainable" in page:
    header(f"Explainable AI & Trust {rtag()}", "Human-centred AI — interpretability first")
    rq(f"RQ3 — Trust->PA Adoption r={sd.corr['trust_pa']} (strongest correlation, n={sd.n})")

    st.markdown(ins(
        f"<strong>Dissertation Finding:</strong> Trust-PA Adoption r=<strong>{sd.corr['trust_pa']}</strong> "
        f"is the strongest correlation. Q17 transparency: only <strong>{sd.q_stats['Q17']['agree']}%</strong> agree "
        f"explanations are clear — lower than trust score ({sd.q_stats['Q16']['agree']}%). "
        f"Interpretability gap = {round(sd.q_stats['Q16']['agree']-sd.q_stats['Q17']['agree'],1)}pp.","i"),
        unsafe_allow_html=True)

    col1,col2=st.columns(2)
    with col1:
        sh("📊 Feature Importance (SHAP-Style)")
        fi=pd.DataFrame([
            {"Feature":"Defect Count","Importance":0.31},
            {"Feature":"Sprint Velocity","Importance":0.24},
            {"Feature":"Req Changes","Importance":0.18},
            {"Feature":"Team Experience","Importance":0.12},
            {"Feature":"Deploy Frequency","Importance":0.09},
            {"Feature":"Team Satisfaction","Importance":0.06},
        ]).sort_values("Importance")
        fig=px.bar(fi,x="Importance",y="Feature",orientation="h",
            color="Importance",color_continuous_scale=["#DBEAFE","#2563EB","#1E3864"],
            text=fi.Importance.apply(lambda v:f"{v:.3f}"))
        fig.update_traces(textposition="outside")
        fig.update_layout(title="Feature Importance",coloraxis_showscale=False)
        st.plotly_chart(tidy(fig), use_container_width=True)

    with col2:
        sh(f"📊 Trust Survey Results (Real n={sd.n})")
        tdata={"Q16 Trust":sd.q_stats["Q16"],"Q17 Transparency":sd.q_stats["Q17"],
               "Q18 Ease":sd.q_stats["Q18"],"Q19 Training":sd.q_stats["Q19"]}
        fig2=go.Figure()
        fig2.add_trace(go.Bar(name="Mean",x=list(tdata.keys()),
            y=[v["mean"] for v in tdata.values()],
            marker_color=C["blue"],text=[f"{v['mean']:.3f}" for v in tdata.values()],
            textposition="outside",yaxis="y"))
        fig2.add_trace(go.Scatter(name="Agree %",x=list(tdata.keys()),
            y=[v["agree"] for v in tdata.values()],mode="lines+markers+text",
            line=dict(color=C["amber"],width=2.5),marker=dict(size=8),
            text=[f"{v['agree']}%" for v in tdata.values()],textposition="top center",
            yaxis="y2"))
        fig2.update_layout(title=f"Trust & Interpretability (n={sd.n})",
            yaxis=dict(title="Mean",range=[3.5,4.5]),
            yaxis2=dict(title="Agree %",range=[60,90],overlaying="y",side="right"),
            legend=dict(orientation="h",y=1.1))
        st.plotly_chart(tidy(fig2), use_container_width=True)

    sh(f"📊 Correlations — Real Primary Data (n={sd.n})")
    cdf2=pd.DataFrame({
        "Relationship":["BI->Success","PA->Success","Trust->Success",f"Trust->PA Adoption (STRONGEST r={sd.corr['trust_pa']})"],
        "r":[sd.corr["bi_success"],sd.corr["pa_success"],sd.corr["trust_success"],sd.corr["trust_pa"]],
    })
    fig3=px.bar(cdf2,x="r",y="Relationship",orientation="h",
        color="r",color_continuous_scale=["#DBEAFE","#2563EB","#1E3864"],text="r")
    fig3.update_traces(texttemplate="r = %{text:.3f}",textposition="outside")
    fig3.add_vline(x=0.5,line_dash="dot",line_color=C["amber"])
    fig3.update_layout(title="Pearson Correlations",coloraxis_showscale=False,xaxis_range=[0,0.82])
    st.plotly_chart(tidy(fig3), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# P6 — AGILE & DEVOPS
# ══════════════════════════════════════════════════════════════════════════════
elif "Agile" in page:
    header("⚡ Agile & DevOps Monitor", "Sprint analytics and delivery tracking")
    rq("RQ1 & RQ2 — Agile/DevOps integration of predictive analytics")

    agile_pct=round(sum(v for k,v in sd.method.items()
                    if any(x in k for x in ['Agile','DevOps','Hybrid']))/sd.n*100,1)
    st.markdown(ins(
        f"<strong>Survey context:</strong> <strong>{agile_pct}%</strong> of n={sd.n} respondents "
        f"work in Agile, DevOps, or Hybrid environments — directly relevant to this module. "
        f"PA tools mean: {sd.pa_mean}/5.0 | Q15 model currency: {sd.q_stats['Q15']['mean']:.3f}/5.0","i"),
        unsafe_allow_html=True)

    # Simulated sprint data
    sprints=[f"S{i+1}" for i in range(12)]
    vel=[58,60,63,61,66,70,67,64,62,61,63,61]
    defs=[22,20,18,21,16,14,13,15,14,14,13,12]
    deps=[3,4,5,4,7,9,10,8,11,12,14,14]
    sat=[3.5,3.6,3.6,3.7,3.7,3.8,3.8,3.9,3.9,4.0,4.0,4.1]

    last_v=vel[-1]; delta=vel[-1]-vel[-2]
    if last_v>=65 and defs[-1]<=11: hs="🟢 GREEN — Healthy";hc="#F0FDF4";hb="#059669"
    elif last_v>=52:                hs="🟡 AMBER — Monitor";hc="#FFFBEB";hb="#D97706"
    else:                           hs="🔴 RED — At Risk";  hc="#FEF2F2";hb="#DC2626"
    st.markdown(f'<div style="background:{hc};border:2px solid {hb};border-radius:12px;'
                f'padding:12px;text-align:center;font-size:18px;font-weight:800;'
                f'color:#1E293B;margin-bottom:16px">{hs}</div>', unsafe_allow_html=True)

    c=st.columns(4)
    c[0].markdown(kpi("Velocity",f"{last_v} pts",f"{'↑' if delta>=0 else '↓'}{abs(delta)}","b"), unsafe_allow_html=True)
    c[1].markdown(kpi("Defects",str(defs[-1]),"this sprint","r"),  unsafe_allow_html=True)
    c[2].markdown(kpi("Deploys",str(deps[-1]),"this sprint","g"),  unsafe_allow_html=True)
    c[3].markdown(kpi("Satisfaction",str(sat[-1]),"/ 5.0","p"),    unsafe_allow_html=True)

    col1,col2=st.columns(2)
    with col1:
        sh("🏃 Sprint Velocity")
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=sprints,y=vel,mode="lines+markers+text",
            line=dict(color=C["blue"],width=2.5),marker=dict(size=7),
            text=vel,textposition="top center",textfont=dict(size=9),
            fill="tozeroy",fillcolor="rgba(37,99,235,.07)"))
        fig.add_trace(go.Scatter(x=sprints,y=[65]*12,mode="lines",name="Planned",
            line=dict(color=C["amber"],width=1.5,dash="dot")))
        fig.update_layout(title="Sprint Velocity — 12 Sprints")
        st.plotly_chart(tidy(fig), use_container_width=True)

    with col2:
        sh("📉 Burndown Chart")
        days=list(range(1,11));ideal=[100-i*10 for i in range(10)]
        actual=[100,91,82,70,65,55,44,38,None,None]
        fig2=go.Figure()
        fig2.add_trace(go.Scatter(x=days,y=ideal,mode="lines",name="Ideal",
            line=dict(color="#CBD5E1",width=1.5,dash="dot")))
        fig2.add_trace(go.Scatter(x=days,y=actual,mode="lines+markers",name="Actual",
            line=dict(color=C["green"],width=2.5),marker=dict(size=7),
            fill="tozeroy",fillcolor="rgba(5,150,105,.07)"))
        fig2.update_layout(title="Sprint Burndown Chart")
        st.plotly_chart(tidy(fig2), use_container_width=True)

    col3,col4=st.columns(2)
    with col3:
        sh("🚀 Deployment Frequency")
        fig3=go.Figure(go.Bar(x=sprints,y=deps,
            marker_color=[C["green"] if v>=10 else C["blue"] if v>=6 else C["amber"] for v in deps],
            text=deps,textposition="outside"))
        fig3.update_layout(title="Deployments per Sprint",bargap=0.3)
        st.plotly_chart(tidy(fig3), use_container_width=True)

    with col4:
        sh("😊 Team Satisfaction")
        fig4=go.Figure(go.Scatter(x=sprints,y=sat,mode="lines+markers",
            line=dict(color=C["purple"],width=2.5),marker=dict(size=7),
            fill="tozeroy",fillcolor="rgba(124,58,237,.07)"))
        fig4.add_hline(y=4.0,line_dash="dot",line_color=C["green"],annotation_text="Target 4.0")
        fig4.update_layout(title="Team Satisfaction Trend",yaxis_range=[2.5,5.2])
        st.plotly_chart(tidy(fig4), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# P7 — ETHICAL GOVERNANCE
# ══════════════════════════════════════════════════════════════════════════════
elif "Ethical" in page:
    header(f"Ethical Governance {rtag()}", "Responsible AI — bias, privacy, transparency")
    rq(f"RQ4 — Q21 privacy {sd.privacy_pct}% · Q20 bias {sd.bias_pct}% concern (n={sd.n})")

    st.markdown(ins(
        f"<strong>Real Survey (n={sd.n}):</strong> <strong>{sd.privacy_pct}%</strong> privacy concern (Q21) · "
        f"<strong>{sd.bias_pct}%</strong> bias concern (Q20). Mainstream anxieties — "
        f"structural governance required, not a compliance afterthought (Williams, 2023).","d"),
        unsafe_allow_html=True)

    checklist=[
        {"item":"Data quality governance protocol","done":True},
        {"item":"SHAP explainability layer active","done":True},
        {"item":"GDPR / data privacy compliance","done":True},
        {"item":"Bias monitoring dashboard enabled","done":True},
        {"item":"Plain-language model explanations","done":False},
        {"item":"Algorithmic governance committee","done":True},
        {"item":"Quarterly fairness audit scheduled","done":False},
        {"item":"Surveillance policy published","done":False},
    ]
    done=sum(1 for c in checklist if c["done"]); score=int(done/len(checklist)*100)
    sc=C["green"] if score>=75 else C["amber"] if score>=50 else C["red"]

    col_s,col_c=st.columns([1,2])
    with col_s:
        sh("🏆 Governance Score")
        st.markdown(f"""
        <div style="text-align:center;padding:20px;background:#fff;border:2px solid {sc};
                    border-radius:16px;margin-bottom:12px">
          <div style="font-size:52px;font-weight:800;color:{sc};
                      font-family:'JetBrains Mono',monospace">{score}%</div>
          <div style="font-size:11px;color:#64748B;margin-top:2px">{done}/{len(checklist)} criteria</div>
        </div>""", unsafe_allow_html=True)
        st.markdown(kpi("Privacy Q21",f"{sd.privacy_pct}%","concern","r"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(kpi("Bias Q20",f"{sd.bias_pct}%","concern","a"), unsafe_allow_html=True)

    with col_c:
        sh("✅ Governance Checklist (R4)")
        for item in checklist:
            ic="✅" if item["done"] else "⬜"
            bg="#F0FDF4" if item["done"] else "#FAFAFA"
            bd="#BBF7D0" if item["done"] else "#E2E8F0"
            st.markdown(f"""<div style="background:{bg};border:1px solid {bd};border-radius:8px;
                padding:9px 13px;margin-bottom:5px;font-size:13px;
                display:flex;align-items:center;gap:8px">
                <span>{ic}</span>
                <span>{'<strong>'+item['item']+'</strong>' if item['done'] else item['item']}</span>
            </div>""", unsafe_allow_html=True)

    col_b1,col_b2=st.columns(2)
    with col_b1:
        sh("📊 Ethics Survey Q20 & Q21")
        edata={"Q20 Bias\nConcern":sd.q_stats["Q20"],"Q21 Privacy\nConcern":sd.q_stats["Q21"]}
        fig=go.Figure(go.Bar(x=list(edata.keys()),
            y=[v["agree"] for v in edata.values()],
            marker_color=[C["red"],C["amber"]],
            text=[f"{v['agree']}%" for v in edata.values()],textposition="outside"))
        fig.update_layout(title=f"Ethical Concern (Real n={sd.n})",yaxis_range=[0,85],bargap=0.5)
        fig.update_yaxes(ticksuffix="%")
        st.plotly_chart(tidy(fig), use_container_width=True)

    with col_b2:
        sh("⚖️ Bias Monitoring")
        feats=["Role-Based","Team Size","Velocity Eq.","Seniority","Comms"]
        scores=[0.12,0.08,0.15,0.22,0.09]
        fig2=go.Figure()
        fig2.add_trace(go.Bar(x=feats,y=scores,
            marker_color=["#DC2626" if s>0.18 else "#D97706" if s>0.12 else "#059669" for s in scores],
            text=[f"{s:.2f}" for s in scores],textposition="outside"))
        fig2.add_trace(go.Scatter(x=feats,y=[0.20]*5,mode="lines",name="Threshold",
            line=dict(color="#94A3B8",dash="dot",width=1.5)))
        fig2.update_layout(title="Bias Score (Lower = Better)",yaxis_range=[0,.30],bargap=0.35)
        st.plotly_chart(tidy(fig2), use_container_width=True)

    st.markdown(ins(
        "<strong>Human-Centred AI:</strong> "
        "<em>'Predictive outputs should support — not replace — managerial judgement. "
        "Human context remains essential for interpreting model alerts.'</em>","s"),
        unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# P8 — ADOPTION GAP
# ══════════════════════════════════════════════════════════════════════════════
elif "Adoption Gap" in page:
    header(f"Adoption-Intention Gap {rtag()}", "Most important dissertation finding")
    rq(f"RQ3 & RQ5 — All numbers real from n={sd.n} survey responses")

    st.markdown(ins(
        f"<strong>Critical Finding (n={sd.n}):</strong> Despite composite means "
        f"{sd.bi_mean}–{sd.pa_mean}/5.0 and {sd.bi_agree_pct}–{sd.pa_agree_pct}% perceived value, "
        f"<strong>{sd.rarely_never_pct}% rarely or never use tools</strong> (Q26). "
        f"Only {sd.freq_pct}% are frequent active users. "
        f"Positive perceptions do not automatically produce embedded adoption.","d"),
        unsafe_allow_html=True)

    c=st.columns(4)
    c[0].markdown(kpi("BI Perceived",f"{sd.bi_agree_pct}%","agree (Q6)","b"),  unsafe_allow_html=True)
    c[1].markdown(kpi("PA Perceived",f"{sd.pa_agree_pct}%","agree (Q11)","g"), unsafe_allow_html=True)
    c[2].markdown(kpi("Frequently",  f"{sd.freq_pct}%",  "active use","a"),   unsafe_allow_html=True)
    c[3].markdown(kpi("Rarely/Never",f"{sd.rarely_never_pct}%","GAP!","r"),   unsafe_allow_html=True)

    col1,col2=st.columns(2)
    with col1:
        sh(f"📊 Q26 Usage Frequency (Real n={sd.n})")
        fdf=pd.DataFrame({"Freq":list(sd.freq.keys()),"n":list(sd.freq.values())})
        fdf["Pct"]=(fdf["n"]/sd.n*100).round(1)
        fig=px.bar(fdf,x="Freq",y="Pct",color="Freq",
            color_discrete_map={"Very Frequently":C["green"],"Frequently":C["blue"],
                                 "Occasionally":C["amber"],"Rarely":C["red"],"Never":"#7F1D1D"},
            text=fdf.Pct.apply(lambda v:f"{v}%"))
        fig.update_traces(textposition="outside")
        fig.update_layout(title=f"Q26: How Frequently? (n={sd.n})",
                          yaxis_range=[0,45],showlegend=False,bargap=0.3)
        fig.update_yaxes(ticksuffix="%")
        st.plotly_chart(tidy(fig), use_container_width=True)

    with col2:
        sh("📊 Perception vs Actual Usage")
        gdf=pd.DataFrame({
            "Category":["BI Perceived\nValue","PA Perceived\nValue",
                        "Frequently/\nVery Freq Use","Rarely/\nNever Use"],
            "Pct":[sd.bi_agree_pct,sd.pa_agree_pct,sd.freq_pct,sd.rarely_never_pct],
            "Type":["Perception","Perception","Actual Usage","Actual Usage"]
        })
        fig2=px.bar(gdf,x="Category",y="Pct",color="Type",
            color_discrete_map={"Perception":C["blue"],"Actual Usage":C["red"]},
            text="Pct")
        fig2.update_traces(texttemplate="%{text}%",textposition="outside")
        fig2.update_layout(title="Adoption-Intention Gap",yaxis_range=[0,90],bargap=0.3,
            legend=dict(orientation="h",y=1.1))
        fig2.update_yaxes(ticksuffix="%")
        st.plotly_chart(tidy(fig2), use_container_width=True)

    sh("🚧 Real Q27 Barriers — Verbatim Respondent Quotes")
    col3,col4=st.columns([1.5,1])
    with col3:
        barrier_cats={"Data Quality":4,"Lack of Skills":3,"High Costs":2,
                      "Resistance to Change":2,"Poor Integration":1,
                      "Privacy Concerns":1,"Interpretability":1,"Other":2}
        bdf=pd.DataFrame({"Barrier":list(barrier_cats.keys()),"n":list(barrier_cats.values())})
        bdf=bdf.sort_values("n",ascending=True)
        fig3=px.bar(bdf,x="n",y="Barrier",orientation="h",
            color="n",color_continuous_scale=["#FECACA","#DC2626","#7F1D1D"],text="n")
        fig3.update_traces(textposition="outside")
        fig3.update_layout(title="Q27 Barrier Categories",coloraxis_showscale=False,xaxis_range=[0,6])
        st.plotly_chart(tidy(fig3), use_container_width=True)

    with col4:
        sh("💬 Verbatim (Q27)")
        for b in sd.barriers[:6]:
            st.markdown(f'<div class="qbox">{b[:120]}{"..." if len(b)>120 else ""}</div>',
                        unsafe_allow_html=True)

    sh("💬 Positive Practitioner Comments (Q28)")
    cols_c=st.columns(2)
    for i, comment in enumerate(sd.comments[:8]):
        with cols_c[i%2]:
            st.markdown(f"""
            <div style="background:#F0FDF4;border-left:3px solid {C['green']};border-radius:6px;
                        padding:8px 12px;margin-bottom:8px;font-size:12px;color:#064E3B;
                        font-style:italic">"{comment[:130]}{'...' if len(comment)>130 else ''}"
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# P9 — PROJECT RISK ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif "Project Risk" in page:
    header("🎯 Project Risk Analysis", "Multi-project risk assessment tool")
    rq("RQ1 & RQ2 — Demonstrate PA concepts from the dissertation")

    st.markdown(ins(
        "Enter project parameters to generate a risk classification, delivery confidence score, "
        "and visual explanation. Directly demonstrates predictive analytics from Chapter 4.","i"),
        unsafe_allow_html=True)

    col_form, col_result = st.columns([1.2, 1.8])
    with col_form:
        sh("📝 Project Parameters")
        with st.form("risk_form"):
            proj_name = st.text_input("Project Name", "My Project")
            sv2  = st.slider("Sprint Velocity",        20, 100, 62)
            dc2  = st.slider("Defect Count",            0,  50, 14)
            te2  = st.slider("Team Experience (yrs)",   1,  10,  5)
            rc2  = st.slider("Requirement Changes",      0,  20,  5)
            dep2 = st.slider("Deploy Frequency/sprint", 1,  30, 10)
            ts2  = st.slider("Team Satisfaction",       1.0, 5.0, 3.8, 0.1)
            submitted = st.form_submit_button("🔮 Analyse Risk", use_container_width=True)

    with col_result:
        if submitted or True:
            rl2, rp2, rs2 = score_risk(sv2, dc2, te2, rc2, dep2, ts2)
            col2 = RISK_COL[rl2]; bg2 = RISK_BG[rl2]
            delivery_conf = round((1 - rp2/2 + sv2/200) * 100, 1)
            delivery_conf = min(95, max(20, delivery_conf))

            sh(f"📊 Risk Assessment: {proj_name}")
            c3=st.columns(3)
            c3[0].markdown(kpi("Risk Level",   rl2,    "Classification","r" if rl2=="High" else "a" if rl2=="Medium" else "g"), unsafe_allow_html=True)
            c3[1].markdown(kpi("Risk Score",   f"{rs2}", "/ 100",        "r" if rs2>60 else "a" if rs2>40 else "g"), unsafe_allow_html=True)
            c3[2].markdown(kpi("Delivery Conf",f"{delivery_conf:.0f}%","forecast","b"), unsafe_allow_html=True)

            # Risk gauge
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=rs2,
                title={"text": "Risk Score", "font": {"size":14}},
                gauge=dict(
                    axis=dict(range=[0,100]),
                    bar=dict(color=col2),
                    steps=[
                        dict(range=[0,35],  color="#D1FAE5"),
                        dict(range=[35,60], color="#FEF3C7"),
                        dict(range=[60,100],color="#FEE2E2"),
                    ],
                    threshold=dict(line=dict(color="black",width=3),
                                   thickness=0.75, value=rs2)
                )
            ))
            fig_g.update_layout(height=240, **{k:v for k,v in THEME.items()
                                               if k not in ['margin']},
                                margin=dict(l=20,r=20,t=40,b=20))
            st.plotly_chart(fig_g, use_container_width=True)

            sh("🔍 Visual Explanation")
            factors = [
                ("Sprint Velocity",     sv2,  100, "Higher velocity reduces risk", "g" if sv2>=65 else "r"),
                ("Defect Count",        dc2,  50,  "Higher defects increase risk",  "r" if dc2>15 else "g"),
                ("Team Experience",     te2,  10,  "Experience reduces risk",        "g" if te2>=5 else "a"),
                ("Requirement Changes", rc2,  20,  "More changes increase risk",     "r" if rc2>8 else "g"),
                ("Deploy Frequency",    dep2, 30,  "Higher frequency reduces risk",  "g" if dep2>=8 else "a"),
                ("Team Satisfaction",   ts2,  5.0, "Higher satisfaction lowers risk","g" if ts2>=4.0 else "r"),
            ]
            for label, val, max_val, desc, cls in factors:
                pct = int(val/max_val*100)
                color = C["green"] if cls=="g" else C["red"] if cls=="r" else C["amber"]
                st.markdown(prog_bar(f"{label}: {val} — {desc}", pct, color),
                            unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# P10 — ADOPTION READINESS
# ══════════════════════════════════════════════════════════════════════════════
elif "Adoption Readiness" in page:
    header("📈 Adoption Readiness Score",
           "Directly supports Trust-Adoption r=.618 dissertation finding")
    rq(f"RQ3 & RQ4 — Trust-Adoption r={sd.corr['trust_pa']} | Adoption gap {sd.rarely_never_pct}%")

    st.markdown(ins(
        f"<strong>Research Foundation:</strong> Trust->PA Adoption r=<strong>{sd.corr['trust_pa']}</strong> "
        f"confirms trust is the primary adoption gateway. This score operationalises "
        f"the four key drivers identified across survey, interview, and literature evidence.","i"),
        unsafe_allow_html=True)

    col_in2, col_out2 = st.columns([1.2, 1.8])
    with col_in2:
        sh("🎛️ Adoption Readiness Inputs")
        trust_in  = st.slider("Trust in PA/BI Tools (%)",    0, 100, 70,
                              help=f"Survey: {sd.q_stats['Q16']['agree']}% trust PA outputs (Q16)")
        dq_in     = st.slider("Data Quality (%)",            0, 100, 50,
                              help="Key barrier from Q27 and interview findings")
        lead_in   = st.slider("Leadership Support (%)",      0, 100, 55,
                              help="Interview: leadership resistance is primary barrier")
        train_in  = st.slider("Training Level (%)",          0, 100, 75,
                              help=f"Survey: {sd.q_stats['Q19']['agree']}% training adequate (Q19)")

        ar_score, ar_label, ar_color = adoption_readiness(trust_in, dq_in, lead_in, train_in)

        st.markdown(f"""
        <div style="background:{ar_color}15;border:2px solid {ar_color};
                    border-radius:14px;padding:20px;text-align:center;margin-top:16px">
          <div style="font-size:11px;font-weight:700;color:#64748B;letter-spacing:.8px;
                      text-transform:uppercase;margin-bottom:5px">Adoption Readiness Score</div>
          <div style="font-size:48px;font-weight:800;color:{ar_color};
                      font-family:'JetBrains Mono',monospace">{ar_score}%</div>
          <div style="font-size:15px;font-weight:700;color:{ar_color};margin-top:4px">
            {ar_label}</div>
        </div>""", unsafe_allow_html=True)

    with col_out2:
        sh("📊 Readiness Breakdown")
        fig_r = go.Figure(go.Bar(
            x=["Trust in Tools","Data Quality","Leadership Support","Training Level"],
            y=[trust_in, dq_in, lead_in, train_in],
            marker_color=[
                C["green"] if trust_in>=70 else C["amber"] if trust_in>=40 else C["red"],
                C["green"] if dq_in>=70   else C["amber"] if dq_in>=40   else C["red"],
                C["green"] if lead_in>=70 else C["amber"] if lead_in>=40 else C["red"],
                C["green"] if train_in>=70 else C["amber"] if train_in>=40 else C["red"],
            ],
            text=[f"{v}%" for v in [trust_in,dq_in,lead_in,train_in]],
            textposition="outside"
        ))
        fig_r.add_hline(y=70, line_dash="dot", line_color=C["green"], annotation_text="High Readiness")
        fig_r.add_hline(y=40, line_dash="dot", line_color=C["amber"], annotation_text="Moderate")
        fig_r.update_layout(title="Adoption Readiness by Factor",
                            yaxis_range=[0,115], bargap=0.35)
        fig_r.update_yaxes(ticksuffix="%")
        st.plotly_chart(tidy(fig_r), use_container_width=True)

        sh(f"📊 vs Survey Benchmark (n={sd.n})")
        bench_df = pd.DataFrame({
            "Factor": ["Trust (Q16)","Transparency (Q17)","Ease of Use (Q18)","Training (Q19)"],
            "Your Score": [trust_in, trust_in-5, (trust_in+train_in)//2, train_in],
            "Survey Agree%": [sd.q_stats["Q16"]["agree"], sd.q_stats["Q17"]["agree"],
                              sd.q_stats["Q18"]["agree"], sd.q_stats["Q19"]["agree"]],
        })
        fig_b = go.Figure()
        fig_b.add_trace(go.Bar(name="Your Score",x=bench_df["Factor"],
            y=bench_df["Your Score"],marker_color=C["blue"],
            text=bench_df["Your Score"].apply(lambda v:f"{v}%"),textposition="outside"))
        fig_b.add_trace(go.Bar(name="Survey Agree%",x=bench_df["Factor"],
            y=bench_df["Survey Agree%"],marker_color=C["green"],
            text=bench_df["Survey Agree%"].apply(lambda v:f"{v}%"),textposition="outside"))
        fig_b.update_layout(barmode="group",title=f"Vs Survey Benchmark (n={sd.n})",
                            yaxis_range=[0,100], legend=dict(orientation="h",y=1.1))
        fig_b.update_yaxes(ticksuffix="%")
        st.plotly_chart(tidy(fig_b), use_container_width=True)

    if ar_score < 40:
        st.markdown(ins("<strong>Low Readiness:</strong> Address data quality first (R1), then build interpretability (R2). Leadership engagement (R5) is critical at this stage.","d"), unsafe_allow_html=True)
    elif ar_score < 71:
        st.markdown(ins("<strong>Moderate Readiness:</strong> Foundation is building. Focus on trust through explainability (R2) and embed tools in Agile ceremonies (R3).","w"), unsafe_allow_html=True)
    else:
        st.markdown(ins("<strong>High Readiness:</strong> Conditions are favourable for full PA adoption. Maintain governance (R4) and keep leadership engaged (R5).","s"), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# P11 — BI MATURITY
# ══════════════════════════════════════════════════════════════════════════════
elif "BI Maturity" in page:
    header("🏗️ BI Maturity Assessment",
           "Watson & Wixom (2007) BI Maturity Model — Chapter 2")
    rq("Chapter 2 & Chapter 5 — BI Maturity Model links to adoption gap")

    st.markdown(ins(
        "The BI Maturity Model (Watson & Wixom, 2007) describes how organisations progress "
        "from basic reporting through diagnostic and predictive capabilities. "
        f"Survey: BI mean {sd.bi_mean}/5.0 — most organisations in the diagnostic-to-predictive zone.","i"),
        unsafe_allow_html=True)

    col1,col2 = st.columns([1.2,1.8])
    with col1:
        sh("🎛️ Maturity Assessment Inputs")
        dash_use = st.slider("Dashboard Usage (%)",      0, 100, 72,
                             help=f"Survey Q6 agree: {sd.q_stats['Q6']['agree']}%")
        analy_use= st.slider("Analytics Adoption (%)",   0, 100, 55,
                             help=f"Survey Q11 agree: {sd.q_stats['Q11']['agree']}%")
        dq_mat   = st.slider("Data Quality (%)",         0, 100, 45,
                             help="Key barrier from Q27 responses")
        gov_mat  = st.slider("Governance Maturity (%)",  0, 100, 40,
                             help="Based on ethics checklist completion")

        bm_score, bm_label, bm_level = bi_maturity(dash_use, analy_use, dq_mat, gov_mat)
        bm_col = C["green"] if bm_label=="Advanced" else C["blue"] if bm_label=="Developing" else C["amber"]

        st.markdown(f"""
        <div style="background:{bm_col}15;border:2px solid {bm_col};
                    border-radius:14px;padding:20px;text-align:center;margin-top:16px">
          <div style="font-size:44px;font-weight:800;color:{bm_col};
                      font-family:'JetBrains Mono',monospace">{bm_score}%</div>
          <div style="font-size:18px;font-weight:800;color:{bm_col};margin-top:4px">
            {bm_label}</div>
          <div style="font-size:12px;color:#64748B;margin-top:4px">BI Maturity Level {bm_level}/5</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        sh("📊 BI Maturity Breakdown")
        factors_bm=["Dashboard Usage","Analytics Adoption","Data Quality","Governance"]
        vals_bm=[dash_use,analy_use,dq_mat,gov_mat]
        fig=go.Figure(go.Bar(x=factors_bm,y=vals_bm,
            marker_color=[C["green"] if v>=75 else C["blue"] if v>=50 else C["amber"] for v in vals_bm],
            text=[f"{v}%" for v in vals_bm],textposition="outside"))
        fig.add_hline(y=75,line_dash="dot",line_color=C["green"],annotation_text="Advanced")
        fig.add_hline(y=50,line_dash="dot",line_color=C["amber"],annotation_text="Developing")
        fig.update_layout(title="BI Maturity Factors",yaxis_range=[0,115],bargap=0.35)
        fig.update_yaxes(ticksuffix="%")
        st.plotly_chart(tidy(fig), use_container_width=True)

        sh("📊 Maturity Distribution — Literature Benchmark")
        mat_df=pd.DataFrame({
            "Level":["L1: Reporting","L2: Monitoring","L3: Diagnostic","L4: Predictive","L5: Prescriptive"],
            "Pct":  [18, 28, 31, 17, 6]
        })
        fig2=px.bar(mat_df,x="Pct",y="Level",orientation="h",
            color="Pct",color_continuous_scale=["#DBEAFE","#2563EB","#1E3864"],text="Pct")
        fig2.update_traces(texttemplate="%{text}%",textposition="outside")
        fig2.update_layout(title="Organisation Maturity Distribution (Watson & Wixom, 2007)",
                           coloraxis_showscale=False,xaxis_range=[0,40])
        fig2.update_xaxes(ticksuffix="%")
        st.plotly_chart(tidy(fig2), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# P12 — INTERVIEW FINDINGS
# ══════════════════════════════════════════════════════════════════════════════
elif "Interview" in page:
    header("💬 Interview Findings Dashboard",
           "Thematic analysis — Senior Developer / Tech Lead")
    rq("Chapter 4.9 — Qualitative Primary Data — Semi-structured Interview")

    st.markdown(ins(
        "The semi-structured interview with a Senior Developer / Tech Lead provided "
        "qualitative depth that corroborates and extends the survey findings. "
        "Five themes emerged through thematic analysis, each mapped to the research questions.","i"),
        unsafe_allow_html=True)

    themes = [
        {
            "icon":"👁️","title":"Theme 1: Improved Visibility",
            "rq":"RQ1, RQ3","priority":"High","color":C["blue"],
            "insight":"BI dashboards materially improved sprint monitoring and bottleneck detection before issues became critical delays.",
            "quote":"Real-time dashboards gave the team early warning of sprint slowdowns that previously only became visible at review meetings.",
            "survey":f"Corroborates Q8 — highest BI item: mean {sd.q_stats['Q8']['mean']:.3f}, {sd.q_stats['Q8']['agree']}% agree.",
            "literature":"Golestanizadeh et al. (2025): BI impact b=0.534 on project performance.",
        },
        {
            "icon":"⚠️","title":"Theme 2: Data Quality as Critical Constraint",
            "rq":"RQ2","priority":"Critical","color":C["red"],
            "insight":"Inconsistency in how team members recorded sprint data and issue resolution times undermined predictive output reliability.",
            "quote":"The predictions were only as good as what the team recorded — garbage in, garbage out was a real daily problem.",
            "survey":f"Confirms Q27 modal barrier (data quality). PA mean: {sd.pa_mean}/5.0 slightly below BI.",
            "literature":"Yang et al. (2021): data completeness and consistency are structural barriers.",
        },
        {
            "icon":"🤝","title":"Theme 3: Trust and Interpretability",
            "rq":"RQ3, RQ4","priority":"High","color":C["amber"],
            "insight":"Conditional trust — predictions used as directional signals, not decision mandates. Trust contingent on explanatory clarity.",
            "quote":"I would act on a forecast if I understood why the system flagged a risk — but not if it was just a number with no context.",
            "survey":f"Mirrors Q16/Q17 divergence: trust {sd.q_stats['Q16']['agree']}% vs transparency {sd.q_stats['Q17']['agree']}%.",
            "literature":"Setiawan (2025): SHAP explainability converts passive trust into active engagement.",
        },
        {
            "icon":"🧑‍💼","title":"Theme 4: Role of Human Judgement",
            "rq":"RQ2, RQ3","priority":"Moderate","color":C["purple"],
            "insight":"Predictive alerts sometimes contextually inappropriate — team morale, planned absences, scope decisions not in metrics.",
            "quote":"The tool flagged a velocity drop that was actually planned — we knew about it but the model did not. It caused unnecessary panic.",
            "survey":"Supports need for unstructured data integration alongside structured metrics.",
            "literature":"Chen et al. (2020); White Rose study (2025): team-level features > code metrics.",
        },
        {
            "icon":"🚧","title":"Theme 5: Organisational Adoption Barriers",
            "rq":"RQ1, RQ5","priority":"Critical","color":C["red"],
            "insight":"Senior management resistance to data-driven governance was a more significant constraint than tool quality.",
            "quote":"Getting buy-in from leadership was harder than implementing the tools. They trusted their experience more than a dashboard.",
            "survey":f"Explains Q26 frequency gap: {sd.rarely_never_pct}% rarely/never use tools.",
            "literature":"Campana & Schott (2018): organisational readiness is the binding constraint.",
        },
    ]

    for t in themes:
        pri_color = C["red"] if t["priority"]=="Critical" else C["amber"] if t["priority"]=="High" else C["blue"]
        st.markdown(f"""
        <div class="icard" style="border-left:5px solid {t['color']}">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <span style="font-size:22px">{t['icon']}</span>
            <span style="font-size:16px;font-weight:700;color:#1E293B">{t['title']}</span>
            <span class="badge badge-b">{t['rq']}</span>
            <span style="background:{pri_color}15;color:{pri_color};border:1px solid {pri_color}40;
                         border-radius:20px;padding:2px 10px;font-size:10px;font-weight:700">
              {t['priority']}</span>
          </div>
          <p style="font-size:13.5px;color:#334155;line-height:1.6;margin-bottom:8px">{t['insight']}</p>
          <div class="qbox">{t['quote']}</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">
            <div style="background:#EFF6FF;border-radius:8px;padding:10px;font-size:12px;color:#1E3A5F">
              <strong>Survey Link:</strong><br>{t['survey']}</div>
            <div style="background:#F0FDF4;border-radius:8px;padding:10px;font-size:12px;color:#064E3B">
              <strong>Literature:</strong><br>{t['literature']}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    # Theme summary chart
    sh("📊 Interview Theme Summary")
    theme_df = pd.DataFrame({
        "Theme":   ["Improved Visibility","Data Quality","Trust/Interpretability",
                    "Human Judgement","Leadership Barriers"],
        "Significance": [85, 95, 90, 75, 92],
        "Priority":["High","Critical","High","Moderate","Critical"],
    })
    fig_t = px.bar(theme_df, x="Significance", y="Theme", orientation="h",
        color="Priority",
        color_discrete_map={"Critical":C["red"],"High":C["amber"],"Moderate":C["blue"]},
        text="Significance")
    fig_t.update_traces(texttemplate="%{text}", textposition="outside")
    fig_t.update_layout(title="Interview Theme Significance",xaxis_range=[0,110],
                        legend=dict(orientation="h",y=1.1))
    st.plotly_chart(tidy(fig_t), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# P13 — RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
elif "Recommendations" in page:
    header("💡 Recommendations Framework", "Five evidence-based recommendations — Chapter 5")
    rq("Chapter 5.5 — All evidence grounded in real n={} survey data".format(sd.n))

    st.markdown(ins(
        "<strong>Implementation Order Matters:</strong> R1 and R2 are foundational prerequisites. "
        "R3–R5 cannot achieve impact without them in place.","i"), unsafe_allow_html=True)

    recs_data = [
        {"id":"R1","title":"Data Quality Governance","layer":"Foundation","priority":1,
         "desc":"Standardise data entry, automated validation pipelines, and regular audits before deploying models.",
         "evidence":f"Modal barrier across all evidence streams (Q27, interview, Yang et al. 2021)",
         "color":C["red"],"impact":95},
        {"id":"R2","title":"Interpretability by Design","layer":"Foundation","priority":2,
         "desc":"Integrate SHAP explainability, confidence intervals, and plain-language explanations as standard.",
         "evidence":f"Trust-Adoption r={sd.corr['trust_pa']}; Q17 transparency {sd.q_stats['Q17']['agree']}%",
         "color":C["amber"],"impact":88},
        {"id":"R3","title":"Agile Workflow Integration","layer":"Enhancement","priority":3,
         "desc":"Embed PA outputs into sprint planning, stand-ups, and retrospectives as structured decision inputs.",
         "evidence":f"{sd.rarely_never_pct}% rarely/never use tools (Q26); interview findings",
         "color":C["blue"],"impact":78},
        {"id":"R4","title":"Ethical Governance","layer":"Enhancement","priority":4,
         "desc":"Establish governance covering bias auditing, GDPR compliance, and transparent data-use communication.",
         "evidence":f"Q21: {sd.privacy_pct}% privacy concern; Q20: {sd.bias_pct}% bias concern",
         "color":C["purple"],"impact":72},
        {"id":"R5","title":"Leadership Culture Change","layer":"Enhancement","priority":5,
         "desc":"Executive-level engagement demonstrating business value through accessible evidence.",
         "evidence":"Interview: leadership resistance identified as primary organisational barrier",
         "color":C["navy"],"impact":65},
    ]

    col_f,col_e=st.columns(2)
    with col_f:
        sh("🏗️ Foundation Layer — Must Come First")
        for r in recs_data[:2]:
            st.markdown(f"""
            <div class="rcard" style="border-left:4px solid {r['color']}">
              <span style="background:{r['color']}15;color:{r['color']};border-radius:20px;
                           padding:2px 9px;font-size:10px;font-weight:700">{r['id']} Foundation</span>
              <div style="font-size:15px;font-weight:700;color:#1E293B;margin:7px 0 5px">{r['title']}</div>
              <div style="font-size:13px;color:#475569;line-height:1.6;margin-bottom:7px">{r['desc']}</div>
              <div style="font-size:11px;color:#94A3B8;font-style:italic">Evidence: {r['evidence']}</div>
            </div>""", unsafe_allow_html=True)

    with col_e:
        sh("⚡ Enhancement Layer — Build on Foundation")
        for r in recs_data[2:]:
            st.markdown(f"""
            <div class="rcard" style="border-left:4px solid {r['color']}">
              <span style="background:{r['color']}15;color:{r['color']};border-radius:20px;
                           padding:2px 9px;font-size:10px;font-weight:700">{r['id']} Enhancement</span>
              <div style="font-size:15px;font-weight:700;color:#1E293B;margin:7px 0 5px">{r['title']}</div>
              <div style="font-size:13px;color:#475569;line-height:1.6;margin-bottom:7px">{r['desc']}</div>
              <div style="font-size:11px;color:#94A3B8;font-style:italic">Evidence: {r['evidence']}</div>
            </div>""", unsafe_allow_html=True)

    sh("📊 Implementation Priority vs Expected Impact")
    pdf2=pd.DataFrame({
        "Recommendation":[f"{r['id']}: {r['title']}" for r in recs_data],
        "Priority":[r["priority"] for r in recs_data],
        "Impact":  [r["impact"]   for r in recs_data],
        "Layer":   [r["layer"]    for r in recs_data],
    })
    fig_p=px.scatter(pdf2,x="Priority",y="Impact",size="Impact",color="Layer",
        color_discrete_map={"Foundation":C["navy"],"Enhancement":C["blue"]},
        text="Recommendation")
    fig_p.update_traces(textposition="top center",textfont_size=11)
    fig_p.update_layout(title="Priority vs Expected Impact",
                        xaxis_title="Implementation Order (1=first)",
                        yaxis_title="Expected Impact (%)",
                        legend=dict(orientation="h",y=1.1))
    st.plotly_chart(tidy(fig_p), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# P14 — FUTURE ROADMAP
# ══════════════════════════════════════════════════════════════════════════════
elif "Future" in page:
    header("🚀 Future Research Roadmap", "Chapter 5.7 — Innovation opportunities")
    rq("Chapter 5.7 — Future research directions and next-generation features")

    roadmap=[
        {"phase":"Phase 1","time":"Now",      "item":"Structured Data PA Models",
         "desc":"Sprint metrics, defect rates, CI/CD data — current implementation","status":"Live"},
        {"phase":"Phase 2","time":"6 months", "item":"NLP Sentiment Analysis",
         "desc":"Retrospective notes and team comms for unstructured signal extraction","status":"Research"},
        {"phase":"Phase 2","time":"6 months", "item":"Real-Time Jira Integration",
         "desc":"Live API for continuous sprint data ingestion and model retraining","status":"Research"},
        {"phase":"Phase 3","time":"12 months","item":"Burnout Early Warning",
         "desc":"Workload imbalance and after-hours commit pattern detection","status":"Planned"},
        {"phase":"Phase 3","time":"12 months","item":"AI Sprint Recommendations",
         "desc":"GPT-powered prescriptive sprint advisor for context-aware guidance","status":"Planned"},
        {"phase":"Phase 4","time":"18 months","item":"Longitudinal Validation Study",
         "desc":"12-24 month tracking to validate adoption-intention gap interventions","status":"Planned"},
        {"phase":"Phase 5","time":"24 months","item":"Federated Ethical AI",
         "desc":"Privacy-preserving federated learning for multi-team predictive models","status":"Future"},
    ]
    sc={"Live":C["green"],"Research":C["blue"],"Planned":C["amber"],"Future":C["purple"]}
    bg={"Live":"#F0FDF4","Research":"#EFF6FF","Planned":"#FFFBEB","Future":"#F5F3FF"}

    for ph in ["Phase 1","Phase 2","Phase 3","Phase 4","Phase 5"]:
        items=[r for r in roadmap if r["phase"]==ph]
        if not items: continue
        st.markdown(f'<div style="font-size:14px;font-weight:700;color:#1E293B;'
                    f'border-left:4px solid {sc.get(items[0]["status"],C["blue"])};'
                    f'padding-left:12px;margin:14px 0 8px">{ph} — {items[0]["time"]}</div>',
                    unsafe_allow_html=True)
        cols=st.columns(len(items))
        for col,item in zip(cols,items):
            s=item["status"]
            with col:
                st.markdown(f"""
                <div style="background:{bg.get(s,'#F8FAFC')};
                            border-left:4px solid {sc.get(s,C['blue'])};
                            border:1px solid {sc.get(s,C['blue'])}30;
                            border-radius:11px;padding:14px 15px">
                  <div style="font-size:10px;font-weight:700;color:{sc.get(s,'#64748B')};
                              text-transform:uppercase;letter-spacing:.5px;margin-bottom:5px">{s}</div>
                  <div style="font-size:13.5px;font-weight:700;color:#1E293B;margin-bottom:5px">
                    {item['item']}</div>
                  <div style="font-size:12px;color:#64748B;line-height:1.5">{item['desc']}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    sh("📅 Research Timeline")
    tl=pd.DataFrame({
        "Item":  ["Structured PA","NLP Sentiment","Jira API","Burnout","AI Advisor","Longitudinal","Federated AI"],
        "Start": [0,3,3,7,7,13,19],
        "Dur":   [24,8,8,8,8,8,6],
        "Status":["Live","Research","Research","Planned","Planned","Planned","Future"],
    })
    fig_t=px.bar(tl,x="Dur",y="Item",base="Start",color="Status",orientation="h",
        color_discrete_map=sc,text="Item")
    fig_t.update_traces(textposition="inside",textfont_color="white",textfont_size=11)
    fig_t.update_layout(title="Innovation Timeline (Months from Now)",
                        xaxis_title="Months",legend=dict(orientation="h",y=1.1),
                        xaxis_range=[0,28])
    st.plotly_chart(tidy(fig_t), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# P15 — GENERATE REPORT
# ══════════════════════════════════════════════════════════════════════════════
elif "Generate Report" in page:
    header("📄 Generate Research Report", "Compile full dissertation findings into PDF")
    rq("Complete research summary — all 10 sections")

    st.markdown(ins(
        f"<strong>Report will include:</strong> Executive Summary, Dataset Overview ({sd.label}), "
        f"Survey Findings (Q6-Q25), Risk Analysis, Correlation Insights, Explainable AI, "
        f"Adoption Readiness, Ethical Governance, Recommendations, and Future Research.","i"),
        unsafe_allow_html=True)

    col_cfg, col_prev = st.columns([1.2, 1.8])
    with col_cfg:
        sh("⚙️ Report Configuration")
        rpt_module = st.selectbox("Focus Module",
            ["All Modules","Executive Dashboard","Survey Findings",
             "Risk Analysis","Recommendations","Future Research"])

        st.markdown(f"""
        <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;
                    padding:14px;font-size:13px;color:#475569;margin-top:12px">
          <strong>Report will include:</strong><br><br>
          ✅ Section 1: Executive Summary<br>
          ✅ Section 2: Dataset Overview ({sd.n} respondents)<br>
          ✅ Section 3: Survey Findings (Q6-Q25)<br>
          ✅ Section 4: Risk Analysis<br>
          ✅ Section 5: Correlation Insights<br>
          ✅ Section 6: Explainable AI Findings<br>
          ✅ Section 7: Adoption Readiness<br>
          ✅ Section 8: Ethical Governance<br>
          ✅ Section 9: Recommendations (R1-R5)<br>
          ✅ Section 10: Future Research<br>
          ✅ Appendix: Verbatim Responses (Q27)
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        gen_btn = st.button("🔄 Generate PDF Report", use_container_width=True, type="primary")

    with col_prev:
        sh("📊 Report Preview — Key Statistics")
        c=st.columns(2)
        c[0].markdown(kpi("Dataset",     f"n={sd.n}", sd.label[:30]+"...", "b"), unsafe_allow_html=True)
        c[1].markdown(kpi("Questions",   "20",        "Q6-Q25 Likert","g"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        c2=st.columns(2)
        c2[0].markdown(kpi("BI Mean",    f"{sd.bi_mean}", "/ 5.0","p"), unsafe_allow_html=True)
        c2[1].markdown(kpi("Trust r",    f"{sd.corr['trust_pa']}", "strongest","a"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        sh("📈 Key Findings Preview")
        findings = [
            (f"BI composite mean: {sd.bi_mean}/5.0",        "b"),
            (f"PA composite mean: {sd.pa_mean}/5.0",        "g"),
            (f"Trust-Adoption r = {sd.corr['trust_pa']}",   "p"),
            (f"{sd.rarely_never_pct}% rarely/never use tools","r"),
            (f"{sd.privacy_pct}% data privacy concern",     "r"),
            (f"{sd.bias_pct}% algorithmic bias concern",    "a"),
        ]
        for text, cls in findings:
            col_map={"b":C["blue"],"g":C["green"],"p":C["purple"],"r":C["red"],"a":C["amber"]}
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:6px 0;
                        border-bottom:1px solid #F1F5F9;font-size:13px;color:#334155">
              <span style="width:10px;height:10px;border-radius:50%;
                           background:{col_map.get(cls,'#94A3B8')};flex-shrink:0"></span>
              {text}
            </div>""", unsafe_allow_html=True)

    if gen_btn:
        with st.spinner("Generating comprehensive report..."):
            rl3, rp3, _ = score_risk(62, 14, 5, 5, 10, 3.8)
            ar3 = adoption_readiness(70, 50, 55, 75)
            pdf_bytes = generate_full_report(sd, rl3, rp3, ar3, None)

        st.success(f"✅ Report generated successfully! Dataset: {sd.label}")
        st.download_button(
            "⬇️ Download Full Research Report PDF",
            data=pdf_bytes,
            file_name=f"PredictiveBI_Research_Report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    st.markdown("---")
    sh("⬇️ Export Raw Data")
    c_csv1, c_csv2 = st.columns(2)
    with c_csv1:
        st.download_button(
            "⬇️ Export Survey Data CSV",
            data=to_csv(sd.df),
            file_name="survey_data.csv",
            mime="text/csv",
        )
    with c_csv2:
        q_stats_df = pd.DataFrame([
            {"Q":k,"Statement":v["label"],"Section":v["section"],
             "Mean":v["mean"],"Agree%":v["agree"],"Neutral%":v["neutral"],
             "Disagree%":v["disagree"],"n":v["n"]}
            for k,v in sd.q_stats.items()
        ])
        st.download_button(
            "⬇️ Export Q-Stats CSV",
            data=to_csv(q_stats_df),
            file_name="question_statistics.csv",
            mime="text/csv",
        )

# ── FOOTER ────────────────────────────────────────────────────────────────────
footer()
