-- ═══════════════════════════════════════════════════════════════════════════
-- AI-Powered Smart Recruitment System
-- Phase 9: Database Schema (SQLite-compatible SQL)
-- ═══════════════════════════════════════════════════════════════════════════
-- Tables:
--   1. job_descriptions
--   2. candidates
--   3. resumes
--   4. parsed_resumes
--   5. ats_scores
--   6. interview_questions
--   7. interview_evaluations
--   8. bias_audit_reports
--   9. pipeline_events (hiring funnel tracking)
--  10. offers
--  11. users (recruiter accounts)
-- ═══════════════════════════════════════════════════════════════════════════

PRAGMA foreign_keys = ON;

-- ─────────────────────────────────────────────────────────────────────────────
-- 1. JOB DESCRIPTIONS
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS job_descriptions (
    jd_id           TEXT PRIMARY KEY,       -- e.g. "JD-001"
    title           TEXT NOT NULL,
    company         TEXT NOT NULL,
    location        TEXT,
    employment_type TEXT DEFAULT 'Full-Time',
    ctc_min_lpa     REAL,
    ctc_max_lpa     REAL,
    experience_min  INTEGER DEFAULT 0,
    experience_max  INTEGER DEFAULT 2,
    department      TEXT,
    status          TEXT DEFAULT 'Active',  -- Active | Closed | Draft
    required_skills TEXT,                   -- JSON array stored as text
    preferred_skills TEXT,
    responsibilities TEXT,
    qualifications  TEXT,
    about_company   TEXT,
    posted_at       TEXT DEFAULT (datetime('now')),
    closed_at       TEXT,
    created_by      TEXT,                   -- FK → users.user_id
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

-- ─────────────────────────────────────────────────────────────────────────────
-- 2. CANDIDATES
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS candidates (
    candidate_id    TEXT PRIMARY KEY,       -- e.g. "CAND-SE-001"
    resume_id       TEXT UNIQUE,            -- e.g. "SE-001" — links to resume
    name            TEXT NOT NULL,
    email           TEXT UNIQUE NOT NULL,
    phone           TEXT,
    linkedin_url    TEXT,
    github_url      TEXT,
    portfolio_url   TEXT,
    address         TEXT,
    city            TEXT,
    state           TEXT,
    role_applied    TEXT,
    jd_id           TEXT,                   -- FK → job_descriptions
    quality_tier    TEXT,                   -- Excellent | Average | Poor
    current_stage   TEXT DEFAULT 'Applied', -- Applied | Parsed | Screened | Shortlisted | HR Call | Technical | Panel | Offer | Joined | Rejected
    pipeline_status TEXT DEFAULT 'Active',  -- Active | Withdrawn | Rejected | Hired
    applied_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now')),
    notes           TEXT,
    FOREIGN KEY (jd_id) REFERENCES job_descriptions(jd_id)
);

-- ─────────────────────────────────────────────────────────────────────────────
-- 3. RESUMES (raw files metadata)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS resumes (
    resume_id       TEXT PRIMARY KEY,
    candidate_id    TEXT,
    file_name       TEXT,
    file_path       TEXT,
    file_format     TEXT DEFAULT 'JSON',    -- JSON | PDF | DOCX
    raw_content     TEXT,                   -- full JSON or extracted text
    uploaded_at     TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
);

-- ─────────────────────────────────────────────────────────────────────────────
-- 4. PARSED RESUMES (output of resume_parser.py)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS parsed_resumes (
    parse_id            TEXT PRIMARY KEY,
    resume_id           TEXT UNIQUE,
    candidate_id        TEXT,
    highest_degree      TEXT,
    institution         TEXT,
    cgpa                REAL,
    cgpa_scale          REAL DEFAULT 10.0,
    years_experience    REAL,
    companies           TEXT,               -- JSON array
    skills_flat         TEXT,               -- JSON array (deduplicated)
    skill_count         INTEGER,
    project_count       INTEGER,
    certification_count INTEGER,
    certification_names TEXT,               -- JSON array
    achievements        TEXT,               -- JSON array
    languages_known     TEXT,               -- JSON array
    english_fluency     TEXT,               -- High | Medium | Low | Unknown
    parsed_at           TEXT DEFAULT (datetime('now')),
    parser_version      TEXT DEFAULT '1.0',
    FOREIGN KEY (resume_id)    REFERENCES resumes(resume_id),
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
);

-- ─────────────────────────────────────────────────────────────────────────────
-- 5. ATS SCORES (output of ats_scoring_engine.py)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ats_scores (
    score_id            TEXT PRIMARY KEY,
    candidate_id        TEXT,
    resume_id           TEXT,
    jd_id               TEXT,
    role_applied        TEXT,
    -- Dimension scores
    score_skills        REAL,
    score_experience    REAL,
    score_projects      REAL,
    score_education     REAL,
    score_certifications REAL,
    score_quality       REAL,
    -- Totals
    ats_score_total     REAL,
    rank_in_role        INTEGER,
    shortlisted         INTEGER DEFAULT 0,  -- 0 | 1
    recommendation      TEXT,
    justification       TEXT,               -- JSON blob
    scored_at           TEXT DEFAULT (datetime('now')),
    engine_version      TEXT DEFAULT '1.0',
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id),
    FOREIGN KEY (resume_id)    REFERENCES resumes(resume_id),
    FOREIGN KEY (jd_id)        REFERENCES job_descriptions(jd_id)
);

-- ─────────────────────────────────────────────────────────────────────────────
-- 6. INTERVIEW QUESTIONS BANK
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS interview_questions (
    question_id         TEXT PRIMARY KEY,   -- e.g. "SE-T-01"
    role                TEXT NOT NULL,
    question_type       TEXT NOT NULL,      -- Technical | Behavioural | Situational
    difficulty          TEXT,               -- Easy | Medium | Hard
    question_text       TEXT NOT NULL,
    expected_answer     TEXT,
    evaluation_criteria TEXT,               -- JSON array
    marks               INTEGER DEFAULT 10,
    rubric_excellent    TEXT,
    rubric_average      TEXT,
    rubric_poor         TEXT,
    created_at          TEXT DEFAULT (datetime('now'))
);

-- ─────────────────────────────────────────────────────────────────────────────
-- 7. INTERVIEW EVALUATIONS
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS interview_evaluations (
    eval_id             TEXT PRIMARY KEY,
    candidate_id        TEXT,
    interviewer_id      TEXT,               -- FK → users.user_id
    interview_round     TEXT,               -- Technical-1 | Technical-2 | HR | Panel
    interview_date      TEXT,
    questions_used      TEXT,               -- JSON array of question_ids
    scores_per_question TEXT,               -- JSON: {question_id: score}
    total_score         REAL,
    max_possible        REAL,
    percentage          REAL,
    overall_assessment  TEXT,               -- Excellent | Good | Average | Poor
    recommendation      TEXT,               -- Proceed | Hold | Reject
    feedback_notes      TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (candidate_id)   REFERENCES candidates(candidate_id),
    FOREIGN KEY (interviewer_id) REFERENCES users(user_id)
);

-- ─────────────────────────────────────────────────────────────────────────────
-- 8. BIAS AUDIT REPORTS
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS bias_audit_reports (
    audit_id            TEXT PRIMARY KEY,
    batch_id            TEXT,               -- e.g. "Summer-2024"
    total_candidates    INTEGER,
    overall_risk_level  TEXT,               -- LOW | MEDIUM | HIGH
    severity_high       INTEGER DEFAULT 0,
    severity_medium     INTEGER DEFAULT 0,
    severity_low        INTEGER DEFAULT 0,
    severity_unobs      INTEGER DEFAULT 0,
    dimensions_json     TEXT,               -- full bias_dimensions JSON
    recommendations_json TEXT,
    generated_at        TEXT DEFAULT (datetime('now')),
    generated_by        TEXT DEFAULT 'bias_detection.py v1.0',
    reviewed_by         TEXT,               -- HR reviewer name
    reviewed_at         TEXT,
    status              TEXT DEFAULT 'Pending Review' -- Pending Review | Reviewed | Action Taken
);

-- ─────────────────────────────────────────────────────────────────────────────
-- 9. PIPELINE EVENTS (Hiring Funnel Tracking)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS pipeline_events (
    event_id            TEXT PRIMARY KEY,
    candidate_id        TEXT,
    from_stage          TEXT,
    to_stage            TEXT,
    event_type          TEXT,               -- Advance | Reject | Withdraw | Offer | Accept | Join
    triggered_by        TEXT DEFAULT 'AI', -- AI | Recruiter | System | Candidate
    notes               TEXT,
    event_at            TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
);

-- ─────────────────────────────────────────────────────────────────────────────
-- 10. OFFERS
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS offers (
    offer_id            TEXT PRIMARY KEY,
    candidate_id        TEXT,
    jd_id               TEXT,
    offered_ctc_lpa     REAL,
    offered_role        TEXT,
    joining_date        TEXT,
    offer_letter_path   TEXT,
    offer_status        TEXT DEFAULT 'Sent', -- Sent | Accepted | Declined | Withdrawn
    sent_at             TEXT DEFAULT (datetime('now')),
    responded_at        TEXT,
    decline_reason      TEXT,
    created_by          TEXT,
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id),
    FOREIGN KEY (jd_id)        REFERENCES job_descriptions(jd_id),
    FOREIGN KEY (created_by)   REFERENCES users(user_id)
);

-- ─────────────────────────────────────────────────────────────────────────────
-- 11. USERS (Recruiters / Hiring Managers / Admins)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    user_id             TEXT PRIMARY KEY,
    name                TEXT NOT NULL,
    email               TEXT UNIQUE NOT NULL,
    role                TEXT DEFAULT 'Recruiter', -- Admin | Recruiter | HiringManager | Interviewer
    department          TEXT,
    is_active           INTEGER DEFAULT 1,
    created_at          TEXT DEFAULT (datetime('now')),
    last_login          TEXT
);

-- ═══════════════════════════════════════════════════════════════════════════
-- INDEXES FOR PERFORMANCE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_candidates_role       ON candidates(role_applied);
CREATE INDEX IF NOT EXISTS idx_candidates_stage      ON candidates(current_stage);
CREATE INDEX IF NOT EXISTS idx_candidates_status     ON candidates(pipeline_status);
CREATE INDEX IF NOT EXISTS idx_ats_scores_role       ON ats_scores(role_applied);
CREATE INDEX IF NOT EXISTS idx_ats_scores_shortlisted ON ats_scores(shortlisted);
CREATE INDEX IF NOT EXISTS idx_ats_scores_total      ON ats_scores(ats_score_total DESC);
CREATE INDEX IF NOT EXISTS idx_pipeline_events_cand  ON pipeline_events(candidate_id);
CREATE INDEX IF NOT EXISTS idx_interview_q_role      ON interview_questions(role);
CREATE INDEX IF NOT EXISTS idx_interview_evals_cand  ON interview_evaluations(candidate_id);

-- ═══════════════════════════════════════════════════════════════════════════
-- SEED: RECRUITER USER
-- ═══════════════════════════════════════════════════════════════════════════

INSERT OR IGNORE INTO users (user_id, name, email, role, department) VALUES
    ('USR-001', 'Shreya Rawat',    'shreya.rawat@technova.com',  'Recruiter',       'Talent Acquisition'),
    ('USR-002', 'Rohan Mehta',     'rohan.mehta@technova.com',   'HiringManager',   'Engineering'),
    ('USR-003', 'Preethi Nair',    'preethi.nair@technova.com',  'HiringManager',   'Product'),
    ('USR-004', 'Admin TalentAI',  'admin@technova.com',          'Admin',           'HR Technology');

-- ═══════════════════════════════════════════════════════════════════════════
-- VIEWS (for Dashboard Queries)
-- ═══════════════════════════════════════════════════════════════════════════

-- Pipeline summary view
CREATE VIEW IF NOT EXISTS v_pipeline_summary AS
SELECT
    c.role_applied,
    COUNT(*) AS total_applied,
    SUM(CASE WHEN a.shortlisted = 1 THEN 1 ELSE 0 END) AS shortlisted,
    SUM(CASE WHEN c.current_stage = 'Technical' THEN 1 ELSE 0 END) AS in_technical,
    SUM(CASE WHEN c.current_stage = 'Panel' THEN 1 ELSE 0 END) AS in_panel,
    SUM(CASE WHEN c.current_stage = 'Offer' THEN 1 ELSE 0 END) AS offered,
    SUM(CASE WHEN c.current_stage = 'Joined' THEN 1 ELSE 0 END) AS joined,
    ROUND(AVG(a.ats_score_total), 1) AS avg_ats_score
FROM candidates c
LEFT JOIN ats_scores a ON c.candidate_id = a.candidate_id
GROUP BY c.role_applied;

-- Candidate ranked view
CREATE VIEW IF NOT EXISTS v_candidates_ranked AS
SELECT
    c.candidate_id, c.name, c.role_applied, c.current_stage, c.quality_tier,
    a.ats_score_total, a.rank_in_role, a.shortlisted, a.recommendation,
    a.score_skills, a.score_experience, a.score_projects,
    a.score_education, a.score_certifications, a.score_quality,
    p.years_experience, p.skill_count, p.certification_count, p.institution, p.cgpa
FROM candidates c
LEFT JOIN ats_scores a    ON c.candidate_id = a.candidate_id
LEFT JOIN parsed_resumes p ON c.candidate_id = p.candidate_id
ORDER BY a.ats_score_total DESC;
