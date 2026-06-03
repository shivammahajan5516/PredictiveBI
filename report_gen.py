# report_gen.py — PDF report generator
# PredictiveBI — Predictive Analytics for Software Project Success

from fpdf import FPDF
from datetime import datetime


def _clean(text):
    """Remove non-latin1 characters."""
    replacements = {
        '\u2014':'--','\u2013':'-','\u2018':"'",'\u2019':"'",
        '\u201c':'"','\u201d':'"','\u2022':'*','\u00e9':'e',
        '\u00e0':'a','\u00e8':'e','\u00f1':'n',
    }
    for u, a in replacements.items():
        text = str(text).replace(u, a)
    return ''.join(c if ord(c) < 256 else '?' for c in text)


class Report(FPDF):
    def __init__(self, dataset_label):
        super().__init__()
        self.dataset_label = dataset_label
        self.set_auto_page_break(auto=True, margin=16)

    def header_bar(self):
        self.set_fill_color(31, 56, 100)
        self.rect(0, 0, 210, 38, 'F')
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.set_y(5)
        self.cell(0, 9, 'PredictiveBI Analytics Report', align='C', ln=True)
        self.set_font('Helvetica', '', 10)
        self.cell(0, 6, 'Predictive Analytics for Software Project Success', align='C', ln=True)
        self.set_font('Helvetica', '', 8)
        self.cell(0, 5, f'Generated: {datetime.now().strftime("%d %b %Y %H:%M")}  |  University of West London  |  Research Prototype', align='C', ln=True)
        self.set_text_color(30, 30, 30)
        self.set_y(45)

    def section_head(self, title, n=None):
        self.set_fill_color(31, 56, 100)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 11)
        label = f'  {f"Section {n}: " if n else ""}{title}'
        self.cell(0, 7, _clean(label), ln=True, fill=True)
        self.set_text_color(30, 30, 30)
        self.ln(2)

    def kv(self, key, value):
        self.set_font('Helvetica', 'B', 10)
        self.cell(72, 6, _clean(str(key)) + ':', ln=False)
        self.set_font('Helvetica', '', 10)
        self.cell(0, 6, _clean(str(value)), ln=True)

    def body(self, text, size=10):
        self.set_font('Helvetica', '', size)
        self.multi_cell(0, 6, _clean(str(text)))
        self.ln(1)

    def table_row(self, values, widths, fill_color=None, bold=False):
        if fill_color:
            self.set_fill_color(*fill_color)
        self.set_font('Helvetica', 'B' if bold else '', 9)
        for v, w in zip(values, widths):
            self.cell(w, 6, _clean(str(v)), border=1, fill=bool(fill_color))
        self.ln()

    def footer(self):
        self.set_y(-14)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(140, 140, 140)
        self.cell(0, 4,
            _clean(f'PredictiveBI -- Predictive Analytics for Software Project Success -- {self.dataset_label}'),
            align='C', ln=True)
        self.cell(0, 4, f'Page {self.page_no()}  |  University of West London  |  Research Prototype',
                  align='C', ln=True)


def generate_full_report(sd, risk_label="N/A", risk_prob=0.0,
                          adopt_score=None, bi_score=None):
    """Generate a comprehensive PDF report from SurveyData sd."""
    pdf = Report(sd.label)
    pdf.add_page()
    pdf.header_bar()

    # ── SECTION 1: Executive Summary ─────────────────────────────────────────
    pdf.section_head('Executive Summary', 1)
    pdf.kv('Dataset', sd.label)
    pdf.kv('Total Respondents', sd.n)
    pdf.kv('BI Composite Mean', f'{sd.bi_mean} / 5.0')
    pdf.kv('PA Composite Mean', f'{sd.pa_mean} / 5.0')
    pdf.kv('Trust Mean', f'{sd.tr_mean} / 5.0')
    pdf.kv('Project Success Mean', f'{sd.suc_mean} / 5.0')
    pdf.kv('Trust --> PA Adoption (r)', f'{sd.corr["trust_pa"]}  [Strongest correlation]')
    pdf.kv('Adoption Gap -- Rarely/Never', f'{sd.rarely_never_pct}%')
    pdf.ln(3)

    # ── SECTION 2: Dataset Overview ───────────────────────────────────────────
    pdf.section_head('Dataset Overview', 2)
    pdf.kv('Roles represented', len(sd.roles))
    pdf.kv('Top role', list(sd.roles.keys())[0] if sd.roles else 'N/A')
    pdf.kv('Top methodology', list(sd.method.keys())[0] if sd.method else 'N/A')
    pdf.kv('Early-career (<=3 yrs)', str(round(
        sum(v for k,v in sd.exp.items() if '1' in k or 'Less' in k) / sd.n * 100, 1)) + '%')
    pdf.kv('Agile/DevOps/Hybrid', str(round(
        sum(v for k,v in sd.method.items()
            if any(x in k for x in ['Agile','DevOps','Hybrid'])) / sd.n * 100, 1)) + '%')
    pdf.ln(3)

    # ── SECTION 3: Survey Findings ────────────────────────────────────────────
    pdf.add_page()
    pdf.section_head('Survey Findings -- Likert Scale Results (Q6-Q25)', 3)
    widths = [14, 72, 20, 20, 24, 20]
    hdrs   = ['Q', 'Statement', 'Mean', 'Agree%', 'Section', 'n']
    pdf.table_row(hdrs, widths, fill_color=(225, 232, 245), bold=True)

    section_colors = {
        'BI':     (219, 234, 254), 'PA':      (237, 233, 254),
        'Trust':  (220, 252, 231), 'Ease':    (254, 249, 195),
        'Ethics': (254, 226, 226), 'Success': (204, 251, 241),
    }
    for qk, qs in sd.q_stats.items():
        sc = qs['section']
        pdf.table_row(
            [qk, qs['label'][:52], f"{qs['mean']:.3f}", f"{qs['agree']}%", sc, qs['n']],
            widths,
            fill_color=section_colors.get(sc, (245, 245, 245))
        )
    pdf.ln(4)

    # ── SECTION 4: Risk Analysis ──────────────────────────────────────────────
    pdf.section_head('Risk Analysis Output', 4)
    pdf.kv('Risk Classification', risk_label)
    pdf.kv('Confidence', f'{risk_prob:.1%}')
    pdf.body('The risk model applies weighted scoring across sprint velocity, defect count, '
             'team experience, requirement changes, deployment frequency, and team satisfaction. '
             'Literature benchmark accuracy: 87.8% (Setiawan, 2025).')

    # ── SECTION 5: Correlation Insights ──────────────────────────────────────
    pdf.add_page()
    pdf.section_head('Correlation Insights (Pearson r)', 5)
    for label, val in [
        ('BI Usage --> Project Success',       sd.corr['bi_success']),
        ('PA Usage --> Project Success',       sd.corr['pa_success']),
        ('Trust --> Project Success',          sd.corr['trust_success']),
        ('Trust --> PA Adoption [STRONGEST]',  sd.corr['trust_pa']),
        ('BI Usage --> PA Adoption',           sd.corr['bi_pa']),
    ]:
        pdf.kv(label, f'r = {val}')
    pdf.ln(2)
    pdf.body('Key Insight: Trust --> PA Adoption (r = ' + str(sd.corr["trust_pa"]) +
             ') is the strongest bivariate correlation, confirming that '
             'interpretability and trust are the primary adoption gateway, '
             'not technical accuracy alone (Davis, 1989; Setiawan, 2025).')

    # ── SECTION 6: Explainable AI ─────────────────────────────────────────────
    pdf.section_head('Explainable AI Findings', 6)
    pdf.kv('Trust in PA outputs (Q16)', f'{sd.q_stats["Q16"]["mean"]:.3f}  ({sd.q_stats["Q16"]["agree"]}% agree)')
    pdf.kv('Clarity of explanations (Q17)', f'{sd.q_stats["Q17"]["mean"]:.3f}  ({sd.q_stats["Q17"]["agree"]}% agree)')
    pdf.kv('Interpretability gap', f'{round(sd.q_stats["Q16"]["agree"]-sd.q_stats["Q17"]["agree"],1)}% (trust > transparency)')
    pdf.body('Implication: One in three practitioners does not find model explanations sufficiently '
             'clear. SHAP-based explainability should be integrated at design stage.')

    # ── SECTION 7: Adoption Readiness ─────────────────────────────────────────
    pdf.section_head('Adoption Readiness Assessment', 7)
    if adopt_score is not None:
        pdf.kv('Adoption Readiness Score', f'{adopt_score[0]}%  -- {adopt_score[1]}')
    pdf.kv('Rarely / Never use tools (Q26)', f'{sd.rarely_never_pct}%')
    pdf.kv('Frequently use tools (Q26)', f'{sd.freq_pct}%')
    pdf.body('The adoption-intention gap shows that positive perceptions do not automatically '
             'produce embedded practice. Multi-level intervention is required.')

    # ── SECTION 8: Ethical Governance ─────────────────────────────────────────
    pdf.add_page()
    pdf.section_head('Ethical Governance Summary', 8)
    pdf.kv('Data privacy concern (Q21)', f'{sd.privacy_pct}%  of respondents')
    pdf.kv('Algorithmic bias concern (Q20)', f'{sd.bias_pct}%  of respondents')
    pdf.body('Ethical concerns are mainstream practitioner anxieties. GDPR transparency '
             'obligations create legal requirements for algorithmic explainability '
             '(Williams, 2023).')

    # ── SECTION 9: Recommendations ────────────────────────────────────────────
    pdf.section_head('Recommendations (Chapter 5)', 9)
    recs = [
        ('R1','Data Quality Governance [Foundation]',
         'Standardise data entry, automated validation, regular audits before deploying models.',
         'Modal barrier across all evidence streams'),
        ('R2','Interpretability by Design [Foundation]',
         'Integrate SHAP explainability, confidence intervals, plain-language explanations.',
         f'Trust-Adoption r={sd.corr["trust_pa"]}; Q17 transparency gap'),
        ('R3','Agile Workflow Integration [Enhancement]',
         'Embed predictive outputs into sprint ceremonies as structured decision inputs.',
         f'{sd.rarely_never_pct}% rarely/never use tools (Q26)'),
        ('R4','Ethical Governance [Enhancement]',
         'Bias auditing, GDPR compliance, transparent data-use communication.',
         f'{sd.privacy_pct}% privacy; {sd.bias_pct}% bias concern'),
        ('R5','Leadership Culture Change [Enhancement]',
         'Executive engagement demonstrating business value through accessible evidence.',
         'Leadership resistance identified as primary organisational barrier'),
    ]
    for rid, rtitle, rdesc, revid in recs:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_fill_color(240, 244, 252)
        pdf.cell(0, 6, _clean(f'  {rid}: {rtitle}'), ln=True, fill=True)
        pdf.set_font('Helvetica', '', 9)
        pdf.multi_cell(0, 5, _clean(f'  {rdesc}'))
        pdf.set_font('Helvetica', 'I', 8)
        pdf.set_text_color(100, 100, 120)
        pdf.cell(0, 5, _clean(f'  Evidence: {revid}'), ln=True)
        pdf.set_text_color(30, 30, 30)
        pdf.ln(1)

    # ── SECTION 10: Future Research ────────────────────────────────────────────
    pdf.add_page()
    pdf.section_head('Future Research Opportunities', 10)
    for item in [
        'NLP Sentiment Analysis -- retrospective notes and team communications',
        'Real-Time Jira Integration -- live sprint data ingestion',
        'Burnout Early-Warning System -- workload and commit pattern detection',
        'AI Sprint Recommendations -- GPT-powered prescriptive advisor',
        'Longitudinal Validation Study -- 12-24 month adoption-intention gap tracking',
        'Multi-Case Study Design -- 6-10 organisations at varying maturity levels',
        'Federated Ethical AI -- privacy-preserving multi-team learning',
    ]:
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(5, 6, '', ln=False)
        pdf.cell(0, 6, _clean(f'* {item}'), ln=True)

    # ── Q27 Barriers ──────────────────────────────────────────────────────────
    if sd.barriers:
        pdf.ln(3)
        pdf.section_head('Appendix: Selected Verbatim Barriers (Q27)')
        for b in sd.barriers[:8]:
            pdf.set_font('Helvetica', 'I', 9)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(0, 5, _clean(f'  "{b[:150]}"'))
            pdf.set_text_color(30, 30, 30)
            pdf.ln(1)

    return bytes(pdf.output())


def to_csv(df):
    return df.to_csv(index=False).encode('utf-8')
