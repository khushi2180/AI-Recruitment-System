# Project Documentation
# AI-Recruitment-System (CV Analysis)
**Date:** July 10, 2026
**Author:** Technical Documentation Agent
**Tech Stack:** Python, Vanilla HTML/CSS/JS, Google Gemini, Groq, Chart.js, PDF.js

## Table of Contents
1. Executive Summary
2. Project Overview
3. Technology Stack
4. Repository Structure
5. Database Documentation / Data Models
6. Complete File Documentation

---

## 1. Executive Summary

### What problem is solved
Modern recruitment teams spend an exorbitant amount of time manually screening resumes, leading to slow hiring cycles, subjective biases, and inefficiencies. The AI-Recruitment-System solves this by providing an automated, AI-driven platform that instantly parses resumes, extracts structured data, and algorithmically scores candidates against specific job requirements.

### Why this project exists
This project exists to streamline the hiring pipeline and empower recruiters with actionable data. By integrating cutting-edge LLMs (Google Gemini 2.0 and Groq Llama 3) with a custom ATS (Applicant Tracking System) scoring engine, the system acts as an intelligent co-pilot. It instantly ranks applicants, generates tailored interview questions, and provides a real-time analytics dashboard to monitor the hiring funnel and detect potential recruitment biases.

### Target users
- **Recruiters & Talent Acquisition:** For uploading bulk resumes, tracking the hiring funnel, and filtering top candidates.
- **Hiring Managers:** For reviewing candidate scores, detailed skill breakdowns, and AI-generated interview questions.
- **HR Leadership:** For monitoring diversity metrics and ensuring unbiased hiring practices via the Bias Detection Report.

### Key features
1. **AI-Powered Resume Parsing:** Leverages Google Gemini and Groq to extract structured JSON data from unstructured PDF resumes.
2. **ATS Scoring Engine:** A sophisticated algorithmic engine that scores candidates out of 100 based on skills (35%), experience (25%), projects (15%), education (10%), certifications (10%), and resume quality (5%).
3. **Dynamic Recruiter Dashboard:** A Vanilla HTML/JS frontend featuring real-time charting (Chart.js), interactive hiring funnels, and dynamic candidate grids.
4. **Bias Detection & Diversity Analytics:** Automatically flags potential hiring biases (e.g., Institution Tier bias, Experience gaps) and provides actionable recommendations.
5. **Interview Question Generator:** Dynamically generates tailored technical, behavioral, and situational questions based on the candidate's specific profile and ATS score.

### Overall architecture
The application follows a lightweight Client-Server architecture:
- **Frontend:** A responsive Single Page Application (SPA) built with Vanilla HTML, CSS, and JavaScript. It uses Chart.js for data visualization and communicates via REST API.
- **Backend:** A custom Python `HTTPServer` (`server.py`) handling file processing, AI provider routing, and API endpoints.
- **Data Layer:** A file-based NoSQL approach where raw and parsed candidate data is persistently stored as structured `.json` files.
- **AI Layer:** Integration with Google Gemini (Primary) and Groq (Fallback) via REST APIs for LLM-based text extraction and reasoning.

### Expected impact
The system is expected to reduce initial resume screening time by over 80%, improve candidate shortlisting accuracy through standardized algorithmic scoring, and actively promote fairer hiring practices by highlighting unconscious biases in the recruitment pipeline.

---

## 2. Project Overview

### Purpose
The purpose of the AI-Recruitment-System is to automate the most tedious aspects of hiring—resume parsing and initial candidate screening—while providing recruiters with a beautiful, data-rich interface to make informed hiring decisions.

### Goals
- Automate the extraction of structured data from unstructured candidate resumes.
- Provide a standardized, objective ATS score for every candidate.
- Visualize the recruitment pipeline and candidate distribution in real-time.

### Objectives
- Parse and score a resume in under 10 seconds.
- Provide fallback AI mechanisms to ensure 99.9% uptime for the parsing engine.
- Deliver an interactive, zero-build-step frontend dashboard.

### Functional Requirements
- **Resume Upload & Parsing:** Support PDF text extraction using `pdfplumber` and LLM parsing.
- **ATS Scoring:** Compare parsed candidate data against predefined `JOB_PROFILES`.
- **Dashboard Analytics:** Display applications received, ATS screened, and shortlisted metrics dynamically.
- **Candidate Management:** View candidate profiles, delete candidates, and dynamically update pipeline counts.
- **Interview Generation:** Generate custom interview questions via LLM prompt engineering.

### Non-functional Requirements
- **Maintainability:** Ensure backend is modular (separating the server from the scoring engine).
- **Usability:** A highly aesthetic, dark-mode focused UI with smooth micro-animations and responsive layout.
- **Resilience:** Automatic fallback from Gemini to Groq if API rate limits are hit.

### Scope
The current scope encompasses the core resume parsing, scoring, and data visualization required for a recruitment cycle. It includes a local file-based database system and integration with external LLM APIs.

### Limitations
- **File-based Database:** Currently relies on local `.json` files rather than a scalable relational database like PostgreSQL.
- **File Format:** Primarily optimized for PDF resumes; complex multi-column images may require OCR which is not natively implemented.

### Future Scope
- **Database Migration:** Transitioning from local JSON files to MongoDB or PostgreSQL for enterprise scale.
- **Email Integration:** Automatically email rejected or shortlisted candidates.
- **Multi-Tenant Architecture:** Supporting multiple companies or distinct hiring campaigns simultaneously.

---

## 3. Technology Stack

### Core Language and Runtime
- **Python 3.x (Backend):** Selected for its robust data processing capabilities, native OS file handling, and excellent ecosystem for AI integration (Gemini/Groq SDKs).
- **JavaScript (Frontend):** Modern Vanilla ES6+ JavaScript used to build a lightweight, dependency-free frontend SPA without the overhead of React or Angular.

### Backend Frameworks and Libraries
- **http.server (Python Standard Library):** Provides a lightweight, custom HTTP server (`RequestHandler`) without the need for heavyweight frameworks like Django, keeping the project highly portable.
- **pdfplumber:** Selected for highly accurate PDF text extraction, preserving layout and column structure better than PyPDF2, which is critical for resume parsing.
- **google-genai & groq:** Official SDKs for interfacing with the respective LLM providers.
- **python-dotenv:** For secure management of API keys and environment variables.

### Frontend Frameworks and Libraries
- **Vanilla HTML/CSS:** A highly customized, Tailwind-inspired utility and component CSS architecture providing a premium "glassmorphism" dark-theme aesthetic.
- **Chart.js (v4.4):** Used for rendering the interactive Shortlist Breakdown donut chart and other potential data visualizations.
- **PDF.js:** Integrated to allow recruiters to view the original PDF resume directly within the browser without downloading it.

### AI & Infrastructure
- **Google Gemini 2.0 Flash Lite (Primary):** Selected for its speed, massive context window, and exceptional JSON-formatting adherence during the resume extraction phase.
- **Groq Llama 3.3 70B (Fallback):** Used as a lightning-fast, high-quality fallback if Gemini hits rate limits (HTTP 429), ensuring uninterrupted system operations.

---

## 4. Repository Structure

The repository is structured as a lightweight full-stack application, cleanly separating data, backend logic, and frontend presentation.

- `/backend/`
  - **Purpose:** Contains core business logic modules independent of the HTTP server.
  - **Key Files:** `ats_scoring_engine.py` (Algorithm for scoring candidates).
- `/dashboard/`
  - **Purpose:** Contains the Frontend SPA.
  - **Key Files:** `index.html` (The unified HTML, CSS, and JS file driving the recruiter dashboard UI), plus an `/assets/` folder for images and icons.
- `/datasets/`
  - **Purpose:** Acts as the local database.
  - **Structure:** 
    - `/resumes/`: Stores the raw generated JSON representations of candidates.
    - `/parsed_resumes/`: Stores aggregated or historically parsed data.
- `/reports/`
  - **Purpose:** Stores generated outputs from the ATS engine (e.g., CSV summaries, ranked JSON reports).
- `server.py`
  - **Purpose:** The main entry point. Runs the Python HTTP server, handles API routing, and executes the AI parsing logic.
- `.env`
  - **Purpose:** Stores sensitive API keys (`GEMINI_API_KEY`, `GROQ_API_KEY`).

---

## 5. Database Documentation / Data Models

The AI-Recruitment-System utilizes a **File-Based NoSQL Architecture**. Instead of a traditional database, candidate records are stored as structured JSON documents. This provides high flexibility for AI-generated schemas.

### Data Types and Normalization
- **Primary Keys:** `resume_id` (e.g., `SE-006`) uniquely identifies candidates, derived from their role prefix and an auto-incrementing index.
- **Schema Enforcement:** The schema is strictly enforced via Prompt Engineering instructions sent to the LLM during parsing, ensuring predictable JSON shapes.

### Core Entity: Candidate JSON Model
The primary data model extracted by the AI and consumed by the frontend:
- **Personal Details:** `name`, `email`, `phone`, `linkedin`, `github`.
- **Role:** `role_applied` (Maps to Job Profiles like Software Engineer, Data Analyst).
- **Education:** Array of objects containing `degree`, `institution`, `cgpa`, and `year_of_passing`.
- **Experience:** Array of objects tracking `company`, `title`, `duration_months`, and `responsibilities`.
- **ATS Score (`ats_score`):**
  - Contains a `total` out of 100.
  - Includes a `breakdown` object detailing sub-scores (`skills_match`, `experience`, `projects`, etc.).
  - Tracks `shortlisted` (Boolean based on threshold >= 65).

---

## 6. Complete File Documentation

### `server.py`
**Purpose:** Acts as the primary backend API server and AI orchestrator.
**Responsibilities:**
- Initializing API clients (Gemini and Groq).
- Extracting raw text from uploaded PDFs via `/api/extract_pdf_text` (using `pdfplumber`).
- Orchestrating the AI parsing via `/api/parse_resume_with_gemini` and handling failovers automatically.
- Providing CRUD operations for the JSON file database (`/api/list_resumes`, `/api/save_resume`, `/api/delete_resume`).
- Generating tailored interview questions based on candidate profiles.
**Optimization & Resilience:** 
- Implements a robust `call_ai` wrapper that catches `RESOURCE_EXHAUSTED` errors from Gemini and seamlessly routes the request to Groq without failing the user request.

### `backend/ats_scoring_engine.py`
**Purpose:** The algorithmic heart of the ATS system.
**Responsibilities:**
- Defines `JOB_PROFILES` with `required_skills`, `preferred_skills`, and minimum thresholds (CGPA, Experience) for various roles.
- The `ATSScoringEngine` class evaluates a parsed resume against the appropriate profile.
- Calculates weighted scores: Skills (35%), Experience (25%), Projects (15%), Education (10%), Certs (10%), Quality (5%).
- Provides rich text justifications for *why* a candidate received a specific score (e.g., matching required vs missing skills).
**Execution Flow:** Can be run independently as a CLI script (`run_ats_engine()`) to aggregate all parsed resumes, rank them, and output a detailed CSV report into `/reports/`.

### `dashboard/index.html`
**Purpose:** The interactive Recruiter Dashboard.
**Responsibilities:**
- **UI/UX:** Implements a premium, animated interface with a dark glassmorphism aesthetic.
- **State Management:** Uses Vanilla JS to manage a global `candidates` array. When data changes (like a deletion or addition), it triggers `applySettings()` and `recalculateKPIs()` to update the DOM globally.
- **Real-Time Data Vis:** Uses Chart.js to render the Shortlist vs Rejected breakdown based on current data.
- **Scrollspy Navigation:** Implements an advanced intersection observer/scroll tracking script to highlight active sections in the sidebar dynamically.
- **Integration:** Calls the Python API endpoints asynchronously via `fetch` to load candidates, trigger parsing, and delete records.

---
*End of Technical Documentation.*
