# Autonomous Data Analyst Agent
### AI-Powered Intelligent Data Analysis Platform

An autonomous, full-stack, enterprise-grade AI data analyst platform that independently ingests structured datasets (CSV, Excel), formulates statistical analysis plans, executes multi-dimensional analytical tools, detects outliers and machine learning anomalies, generates interactive charts, synthesizes actionable business insights, and compiles publication-quality PDF reports.

---

## 🌟 Key Features & Core Modules

### 1. Modern SaaS Analytics Dashboard
- Comprehensive platform telemetry: Total datasets ingested, autonomous analyses completed, insights generated, and dataset quality health index.
- Activity feed of past model runs with status badges and one-click replay.
- Dataset inventory management with quick preview and direct launch CTAs.

### 2. Autonomous Dataset Ingestion & Profiler
- Supports **CSV** and **Excel** (`.xlsx`, `.xls`) with automatic encoding detection (`utf-8`, `latin1`, `iso-8859-1`, `cp1252`).
- Automatically categorizes attributes into **Numerical**, **Categorical**, **Datetime**, **Boolean**, and **Unique Identifiers**.
- Inspects completeness, missing counts, cardinality, sample values, and descriptive metrics.
- Interactive scrollable data preview table.

### 3. Autonomous AI Data Analyst Workflow
Decides analytical steps independently via a 6-stage lifecycle:
1. **Understand Dataset**: Ingests schema and profiles parametric baselines.
2. **Create Analysis Plan**: Determines high-value columns, statistical models, and relevant hypotheses.
3. **Execute Analytical Tools**:
   - `descriptive_statistics`: Parametric metrics, dispersion, skewness, and category breakdowns.
   - `correlation_analyzer`: Pearson correlation matrix and relationship strengths.
   - `trend_analyzer`: Date-based chronology, growth rates, and seasonality.
   - `anomaly_detector`: Multi-dimensional outliers via Scikit-Learn `IsolationForest` and IQR boundaries.
4. **Validate Results**: Verifies non-finite values and correlation boundaries (-1 to +1).
5. **Generate Insights**: Synthesizes business findings with clear categories (Executive Summary, Key Drivers, Trends, Anomalies, Recommendations).
6. **Executive Presentation**: Produces interactive charts and executive dossier.

### 4. Interactive Data Visualizations
Automatically selects goal-oriented charts based on data typology using **Recharts**:
- **Bar Charts**: Categorical aggregations and ranked comparisons.
- **Line Charts**: Temporal trajectory and growth trends over time.
- **Pie / Donut Charts**: Proportional categorical composition.
- **Histograms**: Continuous distribution frequencies and binning.
- **Scatter Plots**: Bivariate correlation and dispersion.
- **Box Plots**: Five-number summaries (Min, Q1, Median, Q3, Max).
- **Correlation Heatmaps**: Pairwise Pearson correlation grid with dynamic color intensity.

### 5. Conversational AI Chat with Your Data
- Ask plain-English questions about the uploaded dataset.
- Dynamic tool calling (`sql_query_engine`, `trend_analyzer`, `anomaly_detector`, `visualization_generator`).
- Answers with calculated metrics—never fabricated numbers.
- Inline interactive charts rendered dynamically inside conversation turns.

### 6. Data Quality & Remediation Studio
- Algorithmic Data Quality Score (0–100) and Letter Grade (A, B, C, D, F).
- Audit of missing cells, duplicate records, and extreme outliers.
- Safe, non-destructive cleaning operations with live **Before & After Impact Previews**:
  - Deduplicate dataset
  - Impute missing values (median/mode)
  - Trim statistical outliers (IQR bounds)
  - Drop sparse columns

### 7. Automated Report Generation
- Multi-section executive intelligence report.
- One-click **Download PDF Dossier** generated via **ReportLab**.
- One-click **Export Analysis CSV**.

### 8. Analysis History & Dataset Comparison
- Persistent history stored in **SQLite**.
- Reopen past analysis sessions with complete logs, charts, and findings.
- Side-by-side **Dataset Comparison Studio** to contrast dimensionality and health across dataset versions.

### 9. Platform Settings & AI Engine
- Configure Google Gemini API key (`gemini-2.0-flash`).
- Fallback parametric statistical NLG engine ensures 100% functionality even in offline mode.
- Engine status monitors for DuckDB, Scikit-learn, and ReportLab.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, TypeScript, Tailwind CSS, Recharts, Lucide React, Vite |
| **Backend** | Python 3.13, FastAPI, Uvicorn, Pydantic, SQLAlchemy |
| **Analytics & ML** | Pandas, NumPy, Scikit-learn (`IsolationForest`), DuckDB |
| **Document Engine**| ReportLab (Vector PDF Generation) |
| **Database** | SQLite (Embedded Relational Store) |
| **AI Integration** | Gemini API (`gemini-2.0-flash`) + Deterministic Statistical Engine |

---

## 📁 Project Structure

```
autonomous-data-analyst/
├── backend/
│   ├── api/
│   │   └── routes.py             # FastAPI REST endpoints
│   ├── agents/
│   │   └── autonomous_analyst.py # Autonomous AI Agent & Chat Reasoner
│   ├── database/
│   │   ├── connection.py         # SQLAlchemy SQLite configuration
│   │   └── seed.py               # Sample dataset generator & seeder
│   ├── models/
│   │   └── models.py             # SQLite database models
│   ├── schemas/
│   │   └── schemas.py            # Pydantic request/response schemas
│   ├── tools/
│   │   ├── dataset_profiler.py       # Column classification & null profiler
│   │   ├── data_quality_checker.py   # Quality scoring & remediation studio
│   │   ├── descriptive_statistics.py # Parametric & group statistics
│   │   ├── correlation_analyzer.py   # Pearson correlation & heatmaps
│   │   ├── trend_analyzer.py         # Chronological resampler & trendline
│   │   ├── anomaly_detector.py       # IsolationForest & IQR detector
│   │   ├── visualization_generator.py# Chart synthesizer
│   │   ├── insight_generator.py      # Business insight NLG engine
│   │   ├── sql_query_engine.py       # DuckDB & SQLite analytical query engine
│   │   └── report_generator.py       # ReportLab PDF & CSV exporter
│   ├── uploads/                  # Ingested dataset store
│   ├── reports/                  # Generated PDF dossiers
│   └── main.py                   # FastAPI server entrypoint
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.tsx       # Navigation drawer & dataset switcher
│   │   │   ├── Navbar.tsx        # Top status bar & analysis trigger
│   │   │   └── ChartRenderer.tsx # Interactive Recharts engine
│   │   ├── pages/
│   │   │   ├── DashboardPage.tsx     # Module 1: Dashboard
│   │   │   ├── UploadPage.tsx        # Module 2: Ingestion & Profiler
│   │   │   ├── AgentPage.tsx         # Module 3: Autonomous AI Agent
│   │   │   ├── VisualizationsPage.tsx# Module 4: Interactive Charts
│   │   │   ├── DataQualityPage.tsx   # Module 6: Quality Studio
│   │   │   ├── ChatPage.tsx          # Module 5: Conversational AI
│   │   │   ├── ReportsPage.tsx       # Module 7: Executive Reports
│   │   │   ├── HistoryPage.tsx       # Module 8: Analysis History & Comparison
│   │   │   └── SettingsPage.tsx      # Module 9: Engine Configuration
│   │   ├── services/
│   │   │   └── api.ts            # Typed API client
│   │   ├── types/
│   │   │   └── index.ts          # TypeScript domain models
│   │   ├── App.tsx               # Main application container
│   │   └── index.css             # Tailwind styling & dark theme
│   ├── package.json
│   └── vite.config.ts
├── .env.example
└── README.md
```

---

## 🚀 Quickstart & Execution Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Configure Environment
Copy `.env.example` to `.env`:
```bash
# In the project root or backend folder
cp .env.example .env
```
*(Optional: Provide `GEMINI_API_KEY` for enhanced LLM reasoning; if left blank, the deterministic parametric statistical engine handles all insights smoothly).*

### 2. Run the Backend API Server
```bash
cd backend
python main.py
```
The FastAPI backend starts at `http://127.0.0.1:8000`.
- API Documentation (Swagger UI): `http://127.0.0.1:8000/docs`

### 3. Run the Frontend Development Server
In a separate terminal:
```bash
cd frontend
npm run dev
```
Open your browser at `http://localhost:5173`.

*Note: Since the production build is compiled in `frontend/dist`, visiting `http://127.0.0.1:8000` will also serve the complete web application directly from FastAPI!*

---

## 🧪 Testing the Complete Pipeline
Run the included end-to-end integration test:
```bash
cd backend
python test_system.py
```
This tests:
1. Dataset ingestion & profiling
2. 6-stage autonomous agent execution
3. Scikit-learn IsolationForest anomaly detection
4. Correlation heatmap computation
5. Visualizations synthesis
6. AI Chat with SQL tool calling
7. PDF report generation and download
8. Data cleaning preview operations
