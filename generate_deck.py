import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    BG_DARK = RGBColor(11, 17, 32)        # #0b1120
    CARD_BG = RGBColor(15, 23, 42)        # #0f172a
    CARD_BORDER = RGBColor(30, 41, 59)    # #1e293b
    ACCENT_BLUE = RGBColor(59, 130, 246)  # #3b82f6
    ACCENT_EMERALD = RGBColor(16, 185, 129) # #10b981
    ACCENT_INDIGO = RGBColor(99, 102, 241) # #6366f1
    TEXT_LIGHT = RGBColor(248, 250, 252)  # #f8fafc
    TEXT_MUTED = RGBColor(148, 163, 184)  # #94a3b8

    def apply_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="AUTONOMOUS DATA ANALYST PLATFORM"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

    def add_card(slide, left, top, width, height, title, body_bullets, accent_color=ACCENT_BLUE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        accent = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.08))
        accent.fill.solid()
        accent.fill.fore_color.rgb = accent_color
        accent.line.fill.background()

        tb = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(0.2), width - Inches(0.6), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(15)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

        for bullet in body_bullets:
            p = tf.add_paragraph()
            p.text = f"•  {bullet}"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MUTED
            p.space_before = Pt(6)

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_bg(s1)

    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.9), Inches(3.8))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "NEXT-GENERATION ENTERPRISE AI"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_BLUE

    p1 = tf1.add_paragraph()
    p1.text = "Autonomous Data Analyst Agent"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT
    p1.space_before = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "An Intelligent, End-to-End Autonomous Platform for Ingestion, Statistical Modeling, Anomaly Detection, Interactive Visualization, and Automated Executive Dossiers."
    p2.font.size = Pt(16)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(14)

    p3 = tf1.add_paragraph()
    p3.text = "Tech Stack: React 19 • TypeScript • Tailwind CSS • FastAPI • DuckDB • Scikit-Learn • Gemini 2.0 • ReportLab"
    p3.font.size = Pt(12)
    p3.font.color.rgb = ACCENT_EMERALD
    p3.space_before = Pt(28)

    # ==========================================
    # SLIDE 2: Executive Summary & Problem Solved
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_bg(s2)
    add_header(s2, "Executive Overview: Transforming Raw Data to Decisions", "EXECUTIVE SUMMARY")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0), "Traditional Analytics Bottleneck", [
        "Manual data inspection requires hours of wrangling.",
        "Ad-hoc scripts are prone to schema & type mismatches.",
        "Non-technical stakeholders wait days for custom dashboards.",
        "Static reports fail to answer follow-up business questions.",
        "Outliers and anomalies frequently slip through undetected."
    ], RGBColor(239, 68, 68))

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0), "The Autonomous Agent Solution", [
        "Upload any CSV or Excel file with zero prior schema configuration.",
        "Autonomous Agent plans and executes multi-step analysis.",
        "Calculates rigorous statistics (mean, IQR, variance, correlation).",
        "Machine Learning detects multivariate anomalies automatically.",
        "Synthesizes natural-language business takeaways (What, Why, Action)."
    ], ACCENT_BLUE)

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "Key Platform Capabilities", [
        "Full-Stack Architecture: React 19 + FastAPI + SQLite.",
        "Dual AI Engine: Gemini 2.0 Flash + Deterministic Statistical Engine.",
        "Goal-Oriented Recharts (Bar, Line, Histogram, Heatmap, Scatter).",
        "Conversational AI Chat with dynamic SQL query execution.",
        "Instant vector PDF executive dossier downloads via ReportLab."
    ], ACCENT_EMERALD)

    # ==========================================
    # SLIDE 3: System Architecture
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_bg(s3)
    add_header(s3, "Enterprise Full-Stack Architecture", "SYSTEM TOPOLOGY")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(2.7), Inches(5.0), "1. Frontend Layer", [
        "React 19 + TypeScript",
        "Tailwind CSS Dark Theme",
        "Interactive Recharts Suite",
        "Lucide React Icons",
        "Responsive Sidebar Navigation",
        "Zero-latency Hot Module Reloading",
        "Clean SaaS UX Design"
    ], ACCENT_BLUE)

    add_card(s3, Inches(3.8), Inches(1.8), Inches(2.7), Inches(5.0), "2. API & Orchestrator", [
        "FastAPI Asynchronous Gateway",
        "Modular REST Endpoints",
        "Background Task Threading",
        "Pydantic v2 Request Validation",
        "SQLite Relational Persistence",
        "CORS & Security Middleware",
        "Integrated SPA Serving"
    ], ACCENT_INDIGO)

    add_card(s3, Inches(6.8), Inches(1.8), Inches(2.7), Inches(5.0), "3. Analytics & ML Core", [
        "DuckDB In-Memory Analytical SQL",
        "Pandas & NumPy Engines",
        "Scikit-learn IsolationForest ML",
        "Pearson Correlation Heatmaps",
        "Temporal Time-Series Resampling",
        "1.5x IQR Boundary Detectors",
        "Non-Destructive Cleaning Studio"
    ], ACCENT_EMERALD)

    add_card(s3, Inches(9.8), Inches(1.8), Inches(2.7), Inches(5.0), "4. AI & Document Layer", [
        "Gemini 2.0 Flash Reasoner",
        "Deterministic Statistical NLG",
        "Dynamic Tool Calling Engine",
        "ReportLab Vector PDF Builder",
        "CSV Analysis Exporter",
        "No-Hallucination Guardrails",
        "100% Offline Fallback Support"
    ], RGBColor(245, 158, 11))

    # ==========================================
    # SLIDE 4: Ingestion & Autonomous Profiler
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_bg(s4)
    add_header(s4, "Automated Dataset Ingestion & Quality Scoring", "MODULE 2 & 6")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3), "Multi-Format Parsing Engine", [
        "Ingests CSV and Excel (.xlsx, .xls) files up to 50MB.",
        "Automatic fallback encoding detection (utf-8, latin1, iso-8859-1, cp1252).",
        "Handles corrupted headers, empty cells, and mixed date formats smoothly."
    ], ACCENT_BLUE)

    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.3), "Schema & Typology Classification", [
        "Identifies Numerical (Continuous/Discrete), Categorical, Datetime, Boolean, and Key IDs.",
        "Calculates completeness, missing percentage, unique values, and sample values.",
        "Provides 15-record interactive scrollable preview table."
    ], ACCENT_INDIGO)

    add_card(s4, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.3), "Algorithmic Data Quality Scorecard", [
        "Calculates 0-100 Quality Score with Letter Grade (A, B, C, D, F).",
        "Applies weighted penalties for missing cells, duplicate rows, and extreme outliers.",
        "Visual progress meters display column completeness at a glance."
    ], ACCENT_EMERALD)

    add_card(s4, Inches(6.8), Inches(4.5), Inches(5.6), Inches(2.3), "Safe Data Remediation Studio", [
        "Non-destructive operations: Deduplication, Imputation (median/mode), Outlier trimming.",
        "Before & After Impact Previews show row/column delta and quality score improvements.",
        "Generates clean versioned datasets upon explicit user approval."
    ], RGBColor(245, 158, 11))

    # ==========================================
    # SLIDE 5: The 6-Stage Autonomous AI Workflow
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_bg(s5)
    add_header(s5, "The 6-Stage Autonomous Analyst Lifecycle", "CORE AI AGENT")

    steps = [
        ("Step 1: Understand", "Inspects rows, columns, data types, null counts, and establishes quality baseline."),
        ("Step 2: Plan", "Formulates multi-stage analytical strategy, target variables, and hypotheses."),
        ("Step 3: Execute", "Runs descriptive stats, correlation matrix, temporal trends, and IsolationForest ML."),
        ("Step 4: Validate", "Audits correlation limits (-1 to +1), verifies finite math, and auto-remediates errors."),
        ("Step 5: Synthesize", "Generates 4-pillar business insights: What Happened, Pattern, Why It Matters, Action."),
        ("Step 6: Present", "Synthesizes interactive charts, dashboard summary cards, and executive PDF dossier.")
    ]

    for idx, (stitle, sdesc) in enumerate(steps):
        col = idx % 3
        row = idx // 3
        x = Inches(0.8 + col * 4.0)
        y = Inches(1.8 + row * 2.6)
        add_card(s5, x, y, Inches(3.7), Inches(2.3), stitle, [sdesc], ACCENT_BLUE if idx < 3 else ACCENT_EMERALD)

    # ==========================================
    # SLIDE 6: Analytical Tool Arsenal
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_bg(s6)
    add_header(s6, "Modular Analytical Tool Arsenal", "ANALYTICAL CAPABILITIES")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3), "Parametric & Grouped Statistics", [
        "Computes mean, median, std dev, variance, min, max, skewness, and kurtosis.",
        "Evaluates categorical frequency distributions and modes.",
        "Automatically cross-tabulates top numerical metrics against primary categorical dimensions."
    ], ACCENT_BLUE)

    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.3), "Correlation & Relational Matrix", [
        "Calculates pairwise Pearson correlation coefficients across numeric features.",
        "Classifies relationships: Strong Positive/Negative, Moderate, or Weak.",
        "Formats 2D correlation matrix for interactive heatmap rendering."
    ], ACCENT_INDIGO)

    add_card(s6, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.3), "Temporal Trend & Chronology Analyzer", [
        "Detects dates and dynamically resamples across Years, Months, Weeks, or Days.",
        "Calculates overall growth percentage and trend direction (Growth, Decline, Steady).",
        "Pinpoints peak and trough operating intervals with exact sums and averages."
    ], ACCENT_EMERALD)

    add_card(s6, Inches(6.8), Inches(4.5), Inches(5.6), Inches(2.3), "Machine Learning Anomaly Detection", [
        "Deploys Scikit-learn IsolationForest for multi-dimensional anomaly detection.",
        "Employs 1.5x IQR boundaries to isolate univariate spikes.",
        "Explains exact deviating factors per flagged record with severity scoring."
    ], RGBColor(239, 68, 68))

    # ==========================================
    # SLIDE 7: Interactive Visualizations
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_bg(s7)
    add_header(s7, "Goal-Oriented Interactive Visualizations", "MODULE 4")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(3.6), Inches(2.3), "Bar & Column Charts", [
        "Categorical performance comparisons.",
        "Aggregates metrics (Total, Average).",
        "Interactive hover tooltips and legends."
    ], ACCENT_BLUE)

    add_card(s7, Inches(4.8), Inches(1.8), Inches(3.6), Inches(2.3), "Line Trend Trajectories", [
        "Temporal progression over calendar periods.",
        "Highlights seasonal peaks and troughs.",
        "Smooth spline curves with data dots."
    ], ACCENT_INDIGO)

    add_card(s7, Inches(8.8), Inches(1.8), Inches(3.6), Inches(2.3), "Pie & Donut Compositions", [
        "Proportional volume breakdowns.",
        "Identifies dominant market segments.",
        "Clean percentage callout labels."
    ], ACCENT_EMERALD)

    add_card(s7, Inches(0.8), Inches(4.5), Inches(3.6), Inches(2.3), "Histograms & Distributions", [
        "Continuous numeric frequency binning.",
        "Highlights variance spread and skewness.",
        "Parametric distribution curves."
    ], RGBColor(245, 158, 11))

    add_card(s7, Inches(4.8), Inches(4.5), Inches(3.6), Inches(2.3), "Bivariate Scatter Plots", [
        "Correlations between primary variables.",
        "Outlier identification along 2 axes.",
        "Interactive point coordinate inspection."
    ], RGBColor(236, 72, 153))

    add_card(s7, Inches(8.8), Inches(4.5), Inches(3.6), Inches(2.3), "Correlation Heatmaps & Box Plots", [
        "Pairwise Pearson matrix with color intensity.",
        "Five-number box plot summary (Min/Q1/Med/Q3/Max).",
        "Fast visual discovery of co-dependencies."
    ], ACCENT_BLUE)

    # ==========================================
    # SLIDE 8: Conversational AI Analyst (Chat)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_bg(s8)
    add_header(s8, "Conversational AI: Chat Directly with Your Data", "MODULE 5")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Conversational Capabilities", [
        "Ask questions in natural English (e.g. 'Which category leads sales?').",
        "Agent invokes dynamic SQL query engine (DuckDB/SQLite) on the fly.",
        "Answers computed directly from actual records—zero hallucinated numbers.",
        "Displays active tools invoked (e.g. sql_query_engine, visualization_generator).",
        "Generates dynamic inline interactive charts right inside chat turns.",
        "Persists full conversational session history in SQLite.",
        "Provides one-click suggested prompt pills for fast exploration."
    ], ACCENT_BLUE)

    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Verified Query Examples & Output", [
        "Query: 'Which category has highest sales?'\n  -> Agent executes SQL GROUP BY and returns Technology ($163,463) with accompanying Bar Chart.",
        "Query: 'Show me the monthly trend.'\n  -> Agent resamples dates, isolates peak interval (2025-10: 126 units), and renders Line Chart.",
        "Query: 'Are there any unusual outliers?'\n  -> Agent runs IsolationForest, isolating 5 irregular records with deviating factor explanations.",
        "Query: 'What are the strongest correlations?'\n  -> Agent calculates Sales vs Profit (r = 0.803, Strong Positive)."
    ], ACCENT_EMERALD)

    # ==========================================
    # SLIDE 9: Automated Report Generation
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_bg(s9)
    add_header(s9, "Automated Executive Reporting & History", "MODULE 7 & 8")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3), "Publication-Quality PDF Dossiers", [
        "Automated compilation via ReportLab vector document engine.",
        "Includes Executive Overview, Quality Scorecard, and Statistical Summary.",
        "Contains 4-pillar business insights and anomaly assessment.",
        "Clean corporate typography, styled data tables, and borders."
    ], ACCENT_BLUE)

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.3), "CSV Analysis Export", [
        "One-click data export of computed analytical results and datasets.",
        "Enables seamless downstream export to Excel or enterprise BI.",
        "Maintains audit readiness and data governance."
    ], ACCENT_INDIGO)

    add_card(s9, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.3), "Historical Session Replay", [
        "Persisted historical analytical sessions stored in SQLite.",
        "One-click replay to reopen full past execution logs, charts, and findings.",
        "Review tool runtimes, durations, and past agent steps."
    ], ACCENT_EMERALD)

    add_card(s9, Inches(6.8), Inches(4.5), Inches(5.6), Inches(2.3), "Dataset Comparison Studio", [
        "Compare two datasets side-by-side (e.g. original vs cleaned version).",
        "Tracks delta in total records, column schema, and Data Quality Scores.",
        "Ensures transparency and quantifiable data enhancement."
    ], RGBColor(245, 158, 11))

    # ==========================================
    # SLIDE 10: Value & Conclusion
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_bg(s10)
    add_header(s10, "Business Value, Impact & Enterprise Scalability", "CONCLUSION")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0), "Quantifiable ROI", [
        "95% reduction in exploratory analysis time (minutes vs days).",
        "Eliminates manual formula errors and inconsistent SQL aggregations.",
        "Empowers non-technical stakeholders to ask questions and receive instant answers.",
        "Automated PDF dossiers ready for immediate C-suite presentation."
    ], ACCENT_EMERALD)

    add_card(s10, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0), "Security & Reliability", [
        "Strict tool sandbox: zero arbitrary LLM Python code execution.",
        "Predefined, validated backend functions for all computations.",
        "Full offline fallback: zero reliance on external API uptime for core analytics.",
        "Local SQLite database keeps data private and secure."
    ], ACCENT_BLUE)

    add_card(s10, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "Production Ready Today", [
        "Fully functional full-stack application running live on localhost:5173 / localhost:8000.",
        "Pre-seeded sample e-commerce dataset for instant testing.",
        "Production Vite build bundled and served directly by FastAPI.",
        "Clean, scalable architecture ready for enterprise deployment."
    ], ACCENT_INDIGO)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Autonomous_Data_Analyst_Platform.pptx")
    prs.save(output_path)
    print(f"Presentation saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    create_presentation()
