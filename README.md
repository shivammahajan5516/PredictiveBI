# PredictiveBI — Enhanced MSc Research Prototype

**Predictive Analytics for Software Project Success: A Business Intelligence Approach**
University of West London | Research Prototype

---

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```
Opens at: http://localhost:8501

---

## Files

```
PredictiveBI/
├── app.py                    Main application (15 modules)
├── helpers.py                CSS, chart helpers, scoring functions
├── loader.py                 Real Excel data loader + upload handler
├── report_gen.py             Full PDF report generator (10 sections)
├── requirements.txt          5 packages only
├── README.md
└── data/
    └── survey_responses.xlsx Real survey data (n=92)
```

---

## Key Features

- Loads real survey Excel automatically on startup
- Upload your own .xlsx or .csv to replace dataset
- All charts update from real data
- 15 modules covering all dissertation chapters
- One dedicated report page (not scattered buttons)
- Full PDF report with 10 sections + verbatim quotes
- Project Risk Analysis with visual gauge
- Adoption Readiness Score (Trust-Adoption r=.618)
- BI Maturity Assessment (Watson & Wixom, 2007)
- Interview Findings with verbatim quotes
- No personal/institutional information in UI
