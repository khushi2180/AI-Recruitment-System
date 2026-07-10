# 🧠 AI-Powered Smart Recruitment System
### Academic Capstone Project — Full AI Hiring Pipeline

---

## 📋 Project Overview

The **AI-Powered Smart Recruitment System** is a complete, demonstration-ready simulation of an enterprise-grade AI hiring platform. Built as a capstone project, it automates the full recruitment lifecycle — from generating job descriptions and parsing resumes to scoring candidates, generating interview questions, detecting bias, and displaying analytics on a recruiter dashboard.

> **This is NOT a document-only project.** Every module runs real Python code against a real dataset of 30 fictional candidates, producing actual scored outputs.

---

## 🏗️ System Architecture

```
                        ┌─────────────────────────┐
                        │   RECRUITER DASHBOARD    │
                        │  dashboard/index.html    │
                        │  (Chart.js + CSS)        │
                        └────────────┬────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │        REST API Layer           │
                    │   docs/api_specification.yaml  │
                    └───┬───────────────────────┬────┘
                        │                       │
           ┌────────────▼──────┐    ┌──────────▼───────────┐
           │  resume_parser.py │    │ ats_scoring_engine.py│
           │  (Phase 3)        │    │ (Phase 4)            │
           └────────────┬──────┘    └──────────┬───────────┘
                        │                       │
           ┌────────────▼──────────────────────▼──┐
           │       bias_detection.py               │
           │       (Phase 6)                       │
           └────────────────────────────────────────┘
                        │
           ┌────────────▼──────────────────────────┐
           │       DATASET LAYER                    │
           │  datasets/resumes/       (30 JSON)     │
           │  datasets/job_descriptions/ (5 JDs)    │
           │  datasets/parsed_resumes/ (30 parsed)  │
           │  datasets/interview_questions/          │
           └────────────────────────────────────────┘
                        │
           ┌────────────▼──────────────────────────┐
           │       DATABASE                         │
           │  database/schema.sql (SQLite)          │
           │  11 tables + views + indexes           │
           └────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
AI-Recruitment-System/
│
├── 📂 backend/
│   ├── resume_parser.py          # Phase 3: Resume parsing engine
│   ├── ats_scoring_engine.py     # Phase 4: ATS scoring + ranking
│   └── bias_detection.py         # Phase 6: Bias audit module
│
├── 📂 datasets/
│   ├── job_descriptions/
│   │   ├── JD_001_Software_Engineer.md
│   │   ├── JD_002_Cyber_Security_Analyst.md
│   │   ├── JD_003_Data_Analyst.md
│   │   ├── JD_004_Product_Manager.md
│   │   └── JD_005_UIUX_Designer.md
│   │
│   ├── resumes/                  # 30 JSON resumes (6 per role)
│   │   ├── SE_001 to SE_006     (Software Engineers)
│   │   ├── CSA_001 to CSA_006   (Cyber Security Analysts)
│   │   ├── DA_001 to DA_006     (Data Analysts)
│   │   ├── PM_001 to PM_006     (Product Managers)
│   │   ├── UX_001 to UX_006     (UI/UX Designers)
│   │   └── MASTER_candidates_index.json
│   │
│   ├── parsed_resumes/           # Output of resume_parser.py
│   │   ├── PARSED_*.json (30 files)
│   │   └── ALL_parsed_resumes.json
│   │
│   └── interview_questions/
│       └── interview_questions_all_roles.json  # 125 questions
│
├── 📂 reports/
│   ├── ats_scores/
│   │   ├── ATS_scores_ranked.json
│   │   └── ATS_scores_summary.csv
│   ├── bias_analysis/
│   │   ├── bias_analysis_results.json
│   │   └── Bias_Audit_Report.txt
│   └── hiring_funnel/
│       └── hiring_funnel_report.json
│
├── 📂 dashboard/
│   └── index.html                # Phase 7: Recruiter Dashboard
│
├── 📂 database/
│   └── schema.sql                # Phase 9: SQLite schema (11 tables)
│
└── 📂 docs/
    └── api_specification.yaml    # Phase 9: OpenAPI 3.0 REST API spec
```

---

## ⚡ Quick Start — Run the Full Pipeline

```bash
# Step 1: Go to project root
cd /Users/krish/Desktop/Khushi/AI-Recruitment-System

# Step 2: Parse all 30 resumes
python3 backend/resume_parser.py

# Step 3: Score and rank all candidates
python3 backend/ats_scoring_engine.py

# Step 4: Run bias detection and generate audit report
python3 backend/bias_detection.py

# Step 5: Open the dashboard
open dashboard/index.html
```

---

## 📊 Phase-by-Phase Summary

| Phase | What Was Built | Files | Status |
|---|---|---|---|
| **Phase 1** | 5 Professional Job Descriptions | `datasets/job_descriptions/*.md` | ✅ Done |
| **Phase 2** | 30 Realistic Candidate Resumes (JSON) | `datasets/resumes/*.json` | ✅ Done |
| **Phase 3** | Resume Parser — Python | `backend/resume_parser.py` | ✅ Done |
| **Phase 4** | ATS Scoring Engine — Python | `backend/ats_scoring_engine.py` | ✅ Done |
| **Phase 5** | 125 Interview Questions with Rubrics | `datasets/interview_questions/` | ✅ Done |
| **Phase 6** | AI Bias Detection + Audit Report | `backend/bias_detection.py` | ✅ Done |
| **Phase 7** | Recruiter Dashboard UI | `dashboard/index.html` | ✅ Done |
| **Phase 8** | Hiring Funnel with 13 Stages | `reports/hiring_funnel/` | ✅ Done |
| **Phase 9** | DB Schema + REST API Spec | `database/` + `docs/` | ✅ Done |

---

## 🧪 Live Results from Running the Pipeline

### ATS Scoring Engine Output
```
ROLE: Cyber Security Analyst
Rank  Name               ATS Score    Skills   Exp    Proj   Edu   Cert  Status
1     Rohan Kapoor       88.4/100     25.9/35  23.7   14.8   10.0  10.0  ✅ SHORTLISTED
2     Arjun Das          78.2/100     15.1/35  24.9   14.2   10.0  10.0  ✅ SHORTLISTED
5     Ananya Sharma      46.6/100      7.5/35  15.0   10.2    9.9   2.5  ❌ REJECTED
6     Snehal Patil       37.6/100      0.0/35  15.0   10.2    8.9   2.5  ❌ REJECTED
```

### Bias Audit Report Summary
```
OVERALL RISK LEVEL: HIGH
  High Severity Dimensions:     4
  Medium Severity Dimensions:   2
  Low Severity Dimensions:      2
  Unobservable Risk:            2

Key Bias Findings:
  Institution Tier Gap:  25.2 pts (Tier-1 vs Tier-3)
  English Fluency Gap:   35.1 pts
  Socioeconomic Gap:     22.4 pts
  Employment Gap:        HIGH severity
```

### Hiring Funnel (Overall)
```
Applications Received  → 30   (100%)
Resumes Parsed by AI   → 30   (100%)
ATS Screened (≥55)     → 22   (73.3%)
Shortlisted (≥65)      → 19   (63.3%)
Interview Scheduled    → 14   (46.7%)
Offers Sent            → 8    (26.7%)
Offers Accepted        → 6    (20.0%)
Day-1 Joiners          → 5    (16.7%)
```

---

## 🔑 Key Technical Decisions

### ATS Scoring Weights
| Dimension | Weight | Justification |
|---|---|---|
| Skills Match | 35% | Primary differentiator; directly maps to JD requirements |
| Experience | 25% | Depth and quality of prior work history |
| Projects | 15% | Demonstrated ability to build and ship |
| Education | 10% | Baseline qualification signal |
| Certifications | 10% | Industry-recognised validation |
| Resume Quality | 5% | Professionalism and completeness |

### Bias Detection Dimensions (10 Total)
1. Gender (proxy-based)
2. College/Institution Tier (**HIGH** — 25.2 pt gap)
3. Age (inferred from grad year)
4. Employment Gap (**HIGH**)
5. English Fluency (**HIGH** — 35.1 pt gap)
6. Socioeconomic Background (**HIGH**)
7. Region/Location (Medium)
8. Resume Length (Low)
9. Disability (Unobservable Risk)
10. Caste/Religion (Unobservable Risk)

---

## 👤 Fictional Candidate Dataset

All 30 candidates are **completely fictional**. Names, emails, institutions, and companies are invented for demonstration purposes.

**Diversity by Design:**
- 10 Excellent candidates (high ATS scores: 80+)
- 10 Average candidates (mid ATS scores: 60–79)
- 10 Poor candidates (low ATS scores: <60)

**Roles (6 per role):**
Software Engineer · Cyber Security Analyst · Data Analyst · Product Manager · UI/UX Designer

---

## 🏆 Dashboard Features

The **Recruiter Dashboard** (`dashboard/index.html`) includes:
- 📊 8 KPI Cards (Applications, Shortlisted, ATS Score, Time-to-Hire, Offers, Interviews…)
- 📉 ATS Score Distribution Bar Chart
- 🏷️ Score by Role (Shortlisted vs Rejected)
- 🔻 7-Stage Hiring Funnel (visual progress bars)
- 🥧 Shortlist/Reject Donut Chart
- 📋 All 30 Candidates Ranked Table with score pills
- 🎯 Role-based Radar Charts (dimension breakdown)
- 🌈 Gender Diversity Bar Chart
- ⚖️ Bias Detection Panel (10 dimensions, severity bars)
- 💼 5 Open Roles with application counts
- 🕐 Live Activity Feed

**Tech:** Pure HTML + CSS (glassmorphism, dark mode, purple theme) + Chart.js
**No framework required** — open `dashboard/index.html` directly in any browser.

---

## 📚 Interview Question Bank

125 total questions across 5 roles:
- **10 Technical questions** per role (with expected answers + code examples)
- **10 Behavioural questions** per role (STAR format rubrics)
- **5 Situational questions** per role (scenario-based)
- Each question: difficulty rating, marks (out of 10), rubric for Excellent/Average/Poor

---

## 📜 Database Schema

SQLite-compatible schema with **11 tables**:
`users` · `job_descriptions` · `candidates` · `resumes` · `parsed_resumes` · `ats_scores` · `interview_questions` · `interview_evaluations` · `bias_audit_reports` · `pipeline_events` · `offers`

Plus: 9 performance indexes + 2 dashboard views (`v_pipeline_summary`, `v_candidates_ranked`)

---

## 🔌 REST API

OpenAPI 3.0 specification (`docs/api_specification.yaml`) with **35+ endpoints** covering:
- `GET/POST /jobs` — Job Description CRUD
- `GET/PATCH /candidates` — Candidate management
- `POST /resumes/parse` — AI parsing
- `POST /ats/score` — ATS scoring
- `GET /ats/rankings/{role}` — Ranked shortlists
- `GET /interviews/questions` — Question bank
- `POST /interviews/evaluations` — Evaluation submission
- `POST /bias/run` — Bias analysis
- `GET /dashboard/*` — Analytics endpoints

---

## 🛡️ Ethics & Bias Mitigation

The system treats bias as a first-class concern:
- **10 bias dimensions** monitored automatically
- **Human-in-the-loop** design — AI assists, humans decide
- **Transparent scoring** — every score has a full justification JSON
- **Audit trail** — all pipeline events logged
- **Recommendations** generated for each bias finding
- **Name-blind review** recommended for all manual stages

---

## 🔧 Requirements

```
Python 3.10+
Standard Library Only (no pip install needed for backend modules)
  - json, re, statistics, datetime, pathlib, typing

Dashboard:
  Browser with internet access (loads Chart.js from CDN)
```

---

*Capstone Project — AI-Powered Smart Recruitment System*
*Built with Python · HTML · CSS · JavaScript · Chart.js · SQLite · OpenAPI*
