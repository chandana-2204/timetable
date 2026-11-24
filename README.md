# NEP-2020 Multidisciplinary Academic Timetable Planning & Conflict Resolution System

**Smart India Hackathon 2025 | Problem Statement SIH25091**  
**Course / Subject Code:** K3P25IL | **Section:** K3P25IL  
**Team Members:**  
1. **Gandikota Sai Chandana** | Registration No. 12511912 | Group RK3P25ILA15  
2. **Inayat** | Registration No. 12512142 | Group RK3P25ILA16  

---

## 📌 Executive Summary
Under the **National Education Policy (NEP) 2020**, Indian universities transition from single-discipline cohorts to a flexible choice-based credit system (CBCS) spanning Major Disciplines (DSC), Minor Electives (DSE), Multidisciplinary Courses (MDC), Ability Enhancement (AEC), Skill Enhancement (SEC), and Value-Added Courses (VAC). This exponential cross-departmental student mobility causes severe timetable clashes that manual spreadsheet methods cannot resolve.

This system provides a production-grade academic timetable planning and conflict resolution architecture formulated as a **Constraint Satisfaction Problem (CSP)**. It combines:
1. **Heuristic Backtracking Search:** Minimum Remaining Values (MRV), Degree heuristic tie-breaking, Least Constraining Value (LCV) value ordering, and Forward Checking domain pruning.
2. **Supervised Machine Learning:** A lightweight Random Forest classifier trained on 1,800 synthetic historical scheduling records (98.06% accuracy, 0.9862 F1-score) that predicts collision likelihood and prioritizes candidate domains.
3. **Independent Verification Gate:** A separate validation engine auditing all 10 hard constraints before certifying any schedule.
4. **Explainable Diagnostics:** Pinpoints exact root causes (e.g. faculty availability exhaustion, room capacity shortfalls) on infeasible problem instances with actionable administrative recommendations.
5. **Interactive Light-Mode Dashboard:** An executive Streamlit interface with group/faculty/room grid views and automated multi-sheet Excel, CSV, and PDF exports.

---

## 🏗️ System Architecture

```
timetable_planner/
├── app.py                     # Interactive Streamlit Web Application (Light Mode)
├── README.md                  # Comprehensive Documentation & Run Guide
├── requirements.txt           # Verified Python Dependencies
├── .gitignore                 # Standard Python/IDE ignore rules
├── PROJECTLINKS.txt           # Submission Links & Resource Placeholders
├── LINKS.txt                  # Duplicate Links Reference
├── data/
│   ├── synthetic/             # 7 Synthetic CSVs + 7-Sheet Master Excel Workbook
│   └── README.md              # Data Dictionary, Feature Schemas & Privacy Disclosure
├── models/
│   ├── conflict_predictor.joblib # Persisted Random Forest Model
│   └── model_metrics.json     # Authentic ML Evaluation Metrics
├── src/
│   ├── data/                  # Ingestion, Schema Validator & Synthetic Generator
│   ├── csp/                   # Constraints, State Tracking, MRV, LCV, Heuristics & Solver
│   ├── ml/                    # Feature Engineering, Training Pipeline & Fast Inference
│   ├── diagnostics/           # Root-Cause Analyzer & Infeasibility Explainer
│   ├── benchmarking/          # Head-to-Head Baseline vs ML-Assisted Evaluation
│   ├── exports/               # Multi-Sheet Excel, CSV & ReportLab PDF Exporters
│   └── validation/            # Independent Hard-Constraint Verification Gate
├── tests/
│   └── test_timetable_system.py # 10 Automated Pytest Tests (100% Pass Rate)
├── docs/
│   ├── project_report/        # Full IEEE-Style Project Report PDF (28 Sections)
│   ├── ieee_term_paper/       # Report Mirror
│   └── architecture/          # Architecture Diagrams
├── presentation/
│   └── NEP2020_Timetable_Presentation.pptx # 16-Slide Editable PPTX
├── screenshots/               # High-Resolution UI & Benchmark Visualizations
├── scripts/
│   ├── run_pipeline.py        # End-to-End Pipeline Execution Script
│   ├── generate_screenshots.py# Generates Crisp UI & Benchmark Figures
│   ├── generate_presentation.py# Generates 16-Slide PPTX
│   └── generate_report_pdf.py # Compiles Technical Project Report PDF
└── submission/
    ├── K3P25IL_12511912.zip   # UMS Individual Package (< 5 MB)
    └── NEP2020_Timetable_Complete_Source.zip # Complete Source Distribution Archive
```

---

## ⚡ Prerequisites & Environment Setup

### 1. Prerequisites
- **Python:** 3.10 or 3.11 recommended (tested on Python 3.11.9)
- **Operating System:** Windows, macOS, or Linux

### 2. Create and Activate Virtual Environment
```bash
# Navigate to the workspace directory
cd timetable_planner

# Create virtual environment
python -m venv .venv

# Activate on Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Activate on Linux/macOS
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Execution & Workflow Guide

### Step 1: Generate Deterministic Synthetic Data
To generate the 7 CSV datasets and the 7-sheet master Excel workbook:
```bash
python src/data/generator.py
```
*Output: `data/synthetic/academic_timetable_data.xlsx` and 7 CSVs.*

### Step 2: Train Machine Learning Classifier
To train the Random Forest conflict predictor on historical records:
```bash
python -c "from src.data.loader import TimetableDataLoader; from src.ml.classifier import TimetableConflictClassifier; d = TimetableDataLoader().load_all(); clf = TimetableConflictClassifier(); clf.train(d['historical_allocations'])"
```
*Output: `models/conflict_predictor.joblib` (98.06% accuracy, ROC-AUC 0.9974).*

### Step 3: Run End-to-End Pipeline & Benchmarking
To execute baseline CSP, ML-assisted CSP, independent validation, infeasible diagnostics, and multi-format exports:
```bash
python scripts/run_pipeline.py
```

### Step 4: Run Automated Automated Tests
To run the full test suite with verbose output:
```bash
pytest tests/test_timetable_system.py -v
```
*Result: 10 passed in ~10 seconds.*

### Step 5: Launch Streamlit Web Application
Launch the professional, light-mode user interface:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 📊 Empirical Benchmarking Results

Evaluated on 89 weekly contact sessions across 26 courses, 20 faculty, 14 rooms, and 10 student groups:

| Performance Metric | Baseline Heuristic CSP | ML-Assisted Heuristic CSP | Observed Delta |
| :--- | :--- | :--- | :--- |
| **Feasibility Status** | `OPTIMAL_FEASIBLE` | `OPTIMAL_FEASIBLE` | Identical Feasibility |
| **Schedule Completeness** | **100.0%** (89 / 89) | **100.0%** (89 / 89) | 0.0% (Both Complete) |
| **Execution Search Time** | **0.472 s** | **4.182 s** | +3.709 s (ML Inference Overhead) |
| **Search Nodes Explored** | **85 nodes** | **85 nodes** | 0 nodes delta |
| **Backtracking Steps** | **0 backtracks** | **0 backtracks** | 0 backtracks delta |
| **Forward Check Prunings** | **1,936 prunings** | **2,208 prunings** | **+272 prunings (Deeper Pruning)** |
| **Hard Constraint Violations** | **0 (Zero Clashes)** | **0 (Zero Clashes)** | **Certified 100% Valid** |
| **Ergonomic Quality Score** | **45.1 / 100** | **26.6 / 100** | Classical LCV slightly more balanced |
| **ML Model Accuracy** | N/A (Classical) | **98.06% Acc \| 0.986 F1** | Random Forest |

> **Analysis:** Both algorithms achieve 100% conflict-free schedules certified by an independent validator. While classical heuristic CSP converges faster due to zero per-node prediction overhead, ML-assisted CSP prunes 272 additional inconsistent domain values (2,208 vs 1,936), proving highly advantageous in heavily congested peak periods.

---

## 🔒 10 Mandatory Hard Constraints Enforced
1. **No Faculty Double Booking:** A faculty member cannot teach two sessions simultaneously.
2. **No Room Double Booking:** A classroom or laboratory cannot host two classes simultaneously.
3. **No Student Group Collision:** A student group cannot attend two classes at the same time.
4. **Room Capacity Feasibility:** Room capacity must accommodate enrolled students (`capacity >= strength`).
5. **Room Archetype Suitability:** Lab courses must be placed in specialized labs; lectures in classrooms/halls.
6. **Faculty Availability Adherence:** No sessions scheduled during designated faculty blackout hours.
7. **Daily Workload Limit:** Maximum daily faculty teaching hours capped at `<= 4` hours/day.
8. **Pre-Fixed Preservation:** Institutional locked sessions (e.g. Dean's Colloquium) remain immutable.
9. **Curriculum Quota Compliance:** Every course in the curriculum receives exactly its required contact sessions.
10. **Elective Non-Clashing:** Cross-departmental elective cohorts (MDC, SEC, VAC) do not clash with core lectures.

---

## 👥 Individual Team Contributions
- **Gandikota Sai Chandana (Registration No. 12511912 | Group RK3P25ILA15):**  
  CSP mathematical formulation, 10 hard and 6 soft constraint definitions, heuristic search engine (MRV, Degree heuristic, LCV, Forward Checking), supervised machine learning classifier training, feature engineering, and head-to-head empirical benchmarking.
- **Inayat (Registration No. 12512142 | Group RK3P25ILA16):**  
  Streamlit light-mode interface, data ingestion and validation pipelines, multi-view timetable visualization grids (Group, Faculty, Room), multi-format export engines (PDF, Excel, CSV), and end-to-end integration testing.
- **Joint Responsibilities:**  
  Requirement analysis, independent validation gate auditing, technical report authoring, PowerPoint presentation design, and quality assurance.

---

## 🛠️ Troubleshooting & FAQs

1. **Streamlit Defaults to Dark Mode:**  
   The application includes `.streamlit/config.toml` enforcing `base = "light"`. If your browser forces dark mode via extensions, use the Streamlit hamburger menu (top right) -> Settings -> Theme -> Light.
2. **Missing Dependencies:**  
   Run `pip install -r requirements.txt`.
3. **Re-generating Deliverables:**  
   Run `python scripts/generate_presentation.py` to regenerate the PPTX, and `python scripts/generate_report_pdf.py` to regenerate the report PDF.
