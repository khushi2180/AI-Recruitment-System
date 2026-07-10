#!/usr/bin/env python3
"""
=============================================================================
AI-Powered Smart Recruitment System
Phase 4: ATS Scoring Engine + Candidate Ranking
=============================================================================
Scores every parsed candidate out of 100 using weighted criteria.
Generates detailed score breakdowns, justifications, and ranked output.

Scoring Weights:
  Skills Match       → 35%
  Experience         → 25%
  Projects           → 15%
  Education          → 10%
  Certifications     → 10%
  Resume Quality     →  5%
  ─────────────────────────
  Total              → 100%
=============================================================================
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR    = Path(__file__).parent.parent
PARSED_DIR  = BASE_DIR / "datasets" / "parsed_resumes"
SCORES_DIR  = BASE_DIR / "reports" / "ats_scores"
SCORES_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# JOB DESCRIPTION PROFILES
# (Defines what each role demands — used to compute skills match)
# ─────────────────────────────────────────────────────────────────────────────

JOB_PROFILES = {
    "Software Engineer": {
        "required_skills": [
            "python", "javascript", "typescript", "react", "node.js", "django",
            "flask", "postgresql", "mysql", "redis", "git", "docker", "rest api",
            "html", "css", "aws", "github", "agile", "scrum", "jest", "pytest"
        ],
        "preferred_skills": [
            "kubernetes", "kafka", "graphql", "microservices", "terraform",
            "grpc", "go", "java", "spring boot", "ci/cd", "github actions"
        ],
        "min_experience_years": 0,
        "max_experience_years": 2,
        "preferred_degree_keywords": ["computer science", "information technology", "software", "cse", "b.tech", "b.e"],
        "preferred_institutions_tier1": ["iit", "bits", "nit", "iiit", "da-iict", "jadavpur", "thapar"],
        "min_cgpa": 6.5,
        "min_projects": 1,
        "valued_certs": ["aws", "kubernetes", "ckad", "cka", "google", "meta", "azure"],
    },

    "Cyber Security Analyst": {
        "required_skills": [
            "splunk", "siem", "mitre att&ck", "nmap", "wireshark", "kali linux",
            "python", "firewall", "tcp/ip", "incident response", "vapt",
            "nessus", "burp suite", "microsoft sentinel", "crowdstrike"
        ],
        "preferred_skills": [
            "oscp", "ceh", "soar", "threat hunting", "digital forensics",
            "volatility", "snort", "metasploit", "ibm qradar", "cloud security",
            "aws security", "active directory", "powershell", "bash"
        ],
        "min_experience_years": 0,
        "max_experience_years": 2,
        "preferred_degree_keywords": ["computer science", "cybersecurity", "information technology", "electronics"],
        "preferred_institutions_tier1": ["iit", "nit", "bits", "manipal", "vit", "jadavpur"],
        "min_cgpa": 6.0,
        "min_projects": 1,
        "valued_certs": ["ceh", "oscp", "security+", "comptia", "cissp", "splunk", "cisa", "ejpt"],
    },

    "Data Analyst": {
        "required_skills": [
            "sql", "python", "pandas", "numpy", "tableau", "power bi",
            "excel", "statistics", "regression", "matplotlib", "seaborn",
            "postgresql", "mysql", "bigquery", "a/b testing", "hypothesis testing"
        ],
        "preferred_skills": [
            "dbt", "airflow", "snowflake", "redshift", "looker", "r",
            "machine learning", "scikit-learn", "spark", "databricks",
            "google analytics", "amplitude", "mixpanel"
        ],
        "min_experience_years": 1,
        "max_experience_years": 3,
        "preferred_degree_keywords": ["statistics", "mathematics", "computer science", "analytics", "economics", "information technology"],
        "preferred_institutions_tier1": ["iit", "iim", "nit", "bits", "osmania", "nirma", "fore", "ibs"],
        "min_cgpa": 6.5,
        "min_projects": 1,
        "valued_certs": ["tableau", "power bi", "pl-300", "google", "aws", "dbt", "microsoft"],
    },

    "Product Manager": {
        "required_skills": [
            "product roadmap", "prd", "user stories", "okr", "backlog",
            "agile", "scrum", "jira", "confluence", "user interviews",
            "a/b testing", "analytics", "stakeholder", "figma", "miro"
        ],
        "preferred_skills": [
            "sql", "mixpanel", "amplitude", "notion", "productboard",
            "rice", "moscow", "kano", "jtbd", "plg", "gtm", "pricing",
            "machine learning concepts", "api", "reforge"
        ],
        "min_experience_years": 3,
        "max_experience_years": 5,
        "preferred_degree_keywords": ["mba", "engineering", "computer science", "technology", "management"],
        "preferred_institutions_tier1": ["iim", "isb", "iit", "nit", "bits", "xlri", "fore", "sibm"],
        "min_cgpa": 6.5,
        "min_projects": 1,
        "valued_certs": ["cspo", "pmp", "aipmm", "reforge", "scrum", "coursera"],
    },

    "UI/UX Designer": {
        "required_skills": [
            "figma", "prototyping", "wireframing", "user research", "usability testing",
            "design system", "ui design", "ux design", "responsive design",
            "mobile design", "typography", "color theory", "accessibility", "wcag"
        ],
        "preferred_skills": [
            "principle", "framer", "after effects", "lottie", "motion design",
            "html", "css", "storybook", "adobe xd", "illustrator", "photoshop",
            "zeplin", "maze", "user testing", "a/b testing"
        ],
        "min_experience_years": 2,
        "max_experience_years": 4,
        "preferred_degree_keywords": ["design", "b.des", "m.des", "visual communication", "interaction", "hci"],
        "preferred_institutions_tier1": ["nid", "iit", "idc", "nift", "pearl academy", "mit institute"],
        "min_cgpa": 6.0,
        "min_projects": 2,
        "valued_certs": ["google ux", "idf", "interaction design", "figma", "certified"],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# ATS SCORING ENGINE
# ─────────────────────────────────────────────────────────────────────────────

class ATSScoringEngine:
    """
    Scores a parsed candidate resume against the relevant job profile.
    Returns a detailed score breakdown with justifications.
    """

    WEIGHTS = {
        "skills_match":   35,
        "experience":     25,
        "projects":       15,
        "education":      10,
        "certifications": 10,
        "resume_quality":  5,
    }

    def __init__(self, parsed_resume: dict):
        self.resume   = parsed_resume
        self.role     = parsed_resume.get("role_applied", "")
        self.profile  = JOB_PROFILES.get(self.role, {})
        self.breakdown = {}
        self.justification = {}

    # ── 1. SKILLS MATCH (35 pts) ──────────────────────────────────────────

    def score_skills(self) -> float:
        max_score = self.WEIGHTS["skills_match"]
        if not self.profile:
            return 0.0

        required   = [s.lower() for s in self.profile.get("required_skills", [])]
        preferred  = [s.lower() for s in self.profile.get("preferred_skills", [])]
        candidate  = [s.lower() for s in self.resume.get("skills_flat", [])]

        # Fuzzy match: check if any candidate skill substring-matches a required skill
        matched_req = [r for r in required if any(r in c or c in r for c in candidate)]
        matched_pref = [p for p in preferred if any(p in c or c in p for c in candidate)]

        req_ratio   = len(matched_req) / max(len(required), 1)
        pref_ratio  = len(matched_pref) / max(len(preferred), 1)

        # 80% weight to required, 20% to preferred
        raw_score = (req_ratio * 0.80 + pref_ratio * 0.20) * max_score
        score     = round(min(raw_score, max_score), 1)

        self.justification["skills_match"] = {
            "score": score,
            "max": max_score,
            "required_matched": matched_req,
            "required_missing": [r for r in required if r not in matched_req],
            "preferred_matched": matched_pref,
            "required_match_rate": f"{len(matched_req)}/{len(required)} ({req_ratio*100:.0f}%)",
            "preferred_match_rate": f"{len(matched_pref)}/{len(preferred)} ({pref_ratio*100:.0f}%)",
        }
        return score

    # ── 2. EXPERIENCE (25 pts) ────────────────────────────────────────────

    def score_experience(self) -> float:
        max_score = self.WEIGHTS["experience"]
        years     = self.resume.get("years_experience", 0.0)
        min_exp   = self.profile.get("min_experience_years", 0)
        max_exp   = self.profile.get("max_experience_years", 2)
        exp_list  = self.resume.get("experience", [])

        # Base score: within range = full; over range = capped; under = proportional
        if years == 0 and min_exp == 0:
            base = 0.60 * max_score          # fresh grad applying to entry role
        elif years < min_exp:
            base = (years / max(min_exp, 1)) * 0.75 * max_score
        elif min_exp <= years <= max_exp:
            base = max_score                  # perfect range
        elif years > max_exp:
            # Overqualified — minor penalty
            base = max_score * 0.90
        else:
            base = 0

        # Bonus: quality signals in responsibilities
        all_resp = " ".join([
            resp for exp in exp_list
            for resp in exp.get("responsibilities", [])
        ]).lower()

        impact_keywords = [
            "reduced", "improved", "increased", "built", "launched", "led",
            "designed", "automated", "saved", "achieved", "delivered", "%",
            "crore", "lakh", "million", "users", "clients", "team"
        ]
        impact_count = sum(1 for kw in impact_keywords if kw in all_resp)
        bonus = min(impact_count * 0.3, 3.0)   # up to 3 bonus points

        score = round(min(base + bonus, max_score), 1)

        self.justification["experience"] = {
            "score": score,
            "max": max_score,
            "years_experience": years,
            "target_range": f"{min_exp}–{max_exp} years",
            "status": (
                "Within target range" if min_exp <= years <= max_exp
                else ("Below minimum" if years < min_exp else "Overqualified")
            ),
            "impact_keywords_detected": impact_count,
            "companies": self.resume.get("companies", []),
        }
        return score

    # ── 3. PROJECTS (15 pts) ──────────────────────────────────────────────

    def score_projects(self) -> float:
        max_score    = self.WEIGHTS["projects"]
        projects     = self.resume.get("projects", [])
        min_projects = self.profile.get("min_projects", 1)
        count        = len(projects)

        if count == 0:
            base = 0.0
        elif count < min_projects:
            base = 0.4 * max_score
        elif count == 1:
            base = 0.65 * max_score
        elif count == 2:
            base = 0.85 * max_score
        else:
            base = max_score

        # Bonus for quality signals: GitHub links, deployment, stars, users
        quality_score = 0
        for proj in projects:
            proj_str = json.dumps(proj).lower()
            if "github" in proj_str or "portfolio" in proj_str:
                quality_score += 0.5
            if any(kw in proj_str for kw in ["stars", "downloads", "users", "deployed", "production"]):
                quality_score += 0.5
            if any(kw in proj_str for kw in ["featured", "award", "open.source", "weekly", "community"]):
                quality_score += 0.5

        bonus = min(quality_score, 3.0)
        score = round(min(base + bonus, max_score), 1)

        self.justification["projects"] = {
            "score": score,
            "max": max_score,
            "project_count": count,
            "min_required": min_projects,
            "project_names": [p.get("name", "") for p in projects],
            "quality_bonus": round(bonus, 1),
        }
        return score

    # ── 4. EDUCATION (10 pts) ─────────────────────────────────────────────

    def score_education(self) -> float:
        max_score = self.WEIGHTS["education"]
        degree    = self.resume.get("highest_degree", "").lower()
        inst      = self.resume.get("institution", "").lower()
        cgpa      = self.resume.get("cgpa")
        min_cgpa  = self.profile.get("min_cgpa", 6.5)

        # Degree level score
        if any(kw in degree for kw in ["ph.d", "phd", "doctorate"]):
            degree_score = max_score
        elif any(kw in degree for kw in ["m.tech", "mba", "m.sc", "m.des", "m.e"]):
            degree_score = max_score * 0.95
        elif any(kw in degree for kw in ["b.tech", "b.e", "b.des", "b.sc", "bca"]):
            degree_score = max_score * 0.85
        elif any(kw in degree for kw in ["b.com", "ba", "diploma"]):
            degree_score = max_score * 0.55
        else:
            degree_score = max_score * 0.60

        # Keyword match to preferred degree types
        pref_keywords = [k.lower() for k in self.profile.get("preferred_degree_keywords", [])]
        if any(kw in degree for kw in pref_keywords):
            degree_score = min(degree_score * 1.1, max_score * 0.95)

        # Institution tier bonus
        tier1_inst = self.profile.get("preferred_institutions_tier1", [])
        inst_bonus = 0.0
        if any(t in inst for t in tier1_inst):
            inst_bonus = 1.0    # Tier-1 bonus

        # CGPA scoring
        cgpa_score = 0.0
        if cgpa is not None:
            if cgpa >= 9.0:
                cgpa_score = 1.5
            elif cgpa >= 8.0:
                cgpa_score = 1.0
            elif cgpa >= min_cgpa:
                cgpa_score = 0.5
            else:
                cgpa_score = -0.5   # Below minimum threshold

        score = round(min(degree_score + inst_bonus + cgpa_score, max_score), 1)

        self.justification["education"] = {
            "score": score,
            "max": max_score,
            "degree": self.resume.get("highest_degree", ""),
            "institution": self.resume.get("institution", ""),
            "cgpa": cgpa,
            "min_cgpa_required": min_cgpa,
            "tier1_institution": any(t in inst for t in tier1_inst),
        }
        return score

    # ── 5. CERTIFICATIONS (10 pts) ────────────────────────────────────────

    def score_certifications(self) -> float:
        max_score   = self.WEIGHTS["certifications"]
        certs       = self.resume.get("certification_names", [])
        valued_certs = [c.lower() for c in self.profile.get("valued_certs", [])]
        cert_count  = len(certs)

        # Match certifications against valued list
        matched = []
        for cert in certs:
            cert_lower = cert.lower()
            if any(vc in cert_lower for vc in valued_certs):
                matched.append(cert)

        if cert_count == 0:
            base = 0.0
        else:
            match_ratio = len(matched) / max(cert_count, 1)
            base = (0.5 + 0.5 * match_ratio) * max_score * min(cert_count / 2.0, 1.0)

        # Prestige bonus for highly valued certs
        prestige_certs = ["oscp", "aws certified solutions architect", "cka", "ckad",
                          "tableau certified", "dbt analytics", "reforge", "iim", "iit"]
        prestige_bonus = sum(
            0.5 for pc in prestige_certs
            if any(pc in c.lower() for c in certs)
        )
        prestige_bonus = min(prestige_bonus, 2.0)

        score = round(min(base + prestige_bonus, max_score), 1)

        self.justification["certifications"] = {
            "score": score,
            "max": max_score,
            "total_certs": cert_count,
            "matched_to_role": matched,
            "all_certs": certs,
            "prestige_bonus": round(prestige_bonus, 1),
        }
        return score

    # ── 6. RESUME QUALITY (5 pts) ─────────────────────────────────────────

    def score_resume_quality(self) -> float:
        max_score = self.WEIGHTS["resume_quality"]
        score     = 0.0
        signals   = []

        # LinkedIn present?
        if self.resume.get("linkedin"):
            score += 0.5; signals.append("LinkedIn present")

        # GitHub/Portfolio present?
        if self.resume.get("github") or self.resume.get("portfolio"):
            score += 0.5; signals.append("GitHub/Portfolio present")

        # Summary quality (longer = more effort)
        summary = (self.resume.get("raw_summary", "") or "").strip()
        # We don't have summary in parsed output — use resume file to check
        if self.resume.get("skill_count", 0) >= 10:
            score += 0.5; signals.append("10+ skills listed")

        # Multiple experience entries?
        if len(self.resume.get("experience", [])) >= 2:
            score += 0.5; signals.append("2+ experience entries")

        # Achievements listed?
        if len(self.resume.get("achievements", [])) >= 2:
            score += 0.5; signals.append("2+ achievements listed")

        # Project with external links?
        for proj in self.resume.get("projects", []):
            if proj.get("github_link") or proj.get("portfolio_link"):
                score += 0.5; signals.append("Project with link")
                break

        # Soft skills and languages listed?
        if self.resume.get("soft_skills") and self.resume.get("languages_known"):
            score += 0.5; signals.append("Soft skills & languages listed")

        # Interests (small bonus for completeness)
        if self.resume.get("interests"):
            score += 0.5; signals.append("Interests listed")

        score = round(min(score, max_score), 1)

        self.justification["resume_quality"] = {
            "score": score,
            "max": max_score,
            "signals_detected": signals,
        }
        return score

    # ── TOTAL SCORE & RESULT ──────────────────────────────────────────────

    def compute(self) -> dict:
        """
        Compute all dimension scores, total ATS score,
        generate justification, and return the full result dict.
        """
        skills_score   = self.score_skills()
        exp_score      = self.score_experience()
        proj_score     = self.score_projects()
        edu_score      = self.score_education()
        cert_score     = self.score_certifications()
        quality_score  = self.score_resume_quality()

        total = round(
            skills_score + exp_score + proj_score +
            edu_score + cert_score + quality_score, 1
        )

        breakdown = {
            "skills_match":   round(skills_score, 1),
            "experience":     round(exp_score, 1),
            "projects":       round(proj_score, 1),
            "education":      round(edu_score, 1),
            "certifications": round(cert_score, 1),
            "resume_quality": round(quality_score, 1),
            "total":          min(total, 100.0),
        }

        # Shortlist threshold: ≥65 AND not zero in skills
        shortlisted = (
            breakdown["total"] >= 65.0 and
            breakdown["skills_match"] >= 10.0
        )

        # Overall recommendation
        if total >= 85:
            recommendation = "STRONGLY RECOMMEND – Excellent match. Priority interview."
        elif total >= 70:
            recommendation = "RECOMMEND – Good match. Schedule interview."
        elif total >= 55:
            recommendation = "CONSIDER – Borderline match. Phone screen first."
        elif total >= 40:
            recommendation = "WEAK – Significant gaps. May not be suitable."
        else:
            recommendation = "REJECT – Insufficient match for this role."

        return {
            "resume_id":       self.resume.get("resume_id", ""),
            "name":            self.resume.get("name", ""),
            "role_applied":    self.role,
            "quality_tier":    self.resume.get("quality_tier", ""),
            "ats_score":       breakdown["total"],
            "breakdown":       breakdown,
            "justification":   self.justification,
            "shortlisted":     shortlisted,
            "recommendation":  recommendation,
            "scored_at":       datetime.now().isoformat(),
        }


# ─────────────────────────────────────────────────────────────────────────────
# RANKING ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def rank_candidates(scored_candidates: list[dict]) -> dict[str, list[dict]]:
    """
    Group candidates by role and rank them within each group.
    Returns a dict keyed by role name.
    """
    grouped: dict[str, list] = {}
    for c in scored_candidates:
        role = c.get("role_applied", "Unknown")
        grouped.setdefault(role, []).append(c)

    ranked = {}
    for role, candidates in grouped.items():
        sorted_list = sorted(candidates, key=lambda x: x["ats_score"], reverse=True)
        for i, c in enumerate(sorted_list, 1):
            c["rank"] = i
        ranked[role] = sorted_list

    return ranked


# ─────────────────────────────────────────────────────────────────────────────
# REPORT PRINTER
# ─────────────────────────────────────────────────────────────────────────────

def print_ranked_report(ranked: dict[str, list[dict]]) -> None:
    print(f"\n{'='*80}")
    print(f"  ATS SCORING ENGINE — RANKED CANDIDATE REPORT")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")

    for role, candidates in ranked.items():
        print(f"\n  {'─'*76}")
        print(f"  ROLE: {role}")
        print(f"  {'─'*76}")
        print(f"  {'Rank':<6} {'Name':<22} {'ATS Score':<12} {'Skills':<10} {'Exp':<8} {'Proj':<8} {'Edu':<7} {'Cert':<7} {'Qual':<6} {'Status':<12}")
        print(f"  {'─'*76}")
        for c in candidates:
            b = c["breakdown"]
            status = "✅ SHORTLISTED" if c["shortlisted"] else "❌ REJECTED"
            print(
                f"  {c['rank']:<6} {c['name']:<22} "
                f"{b['total']:>6.1f}/100   "
                f"{b['skills_match']:>5.1f}/35  "
                f"{b['experience']:>4.1f}/25  "
                f"{b['projects']:>4.1f}/15  "
                f"{b['education']:>4.1f}/10  "
                f"{b['certifications']:>4.1f}/10  "
                f"{b['resume_quality']:>3.1f}/5  "
                f"{status}"
            )
        print()

    print(f"{'='*80}\n")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN RUNNER
# ─────────────────────────────────────────────────────────────────────────────

def run_ats_engine() -> dict:
    """
    Load all parsed resumes → score each one → rank by role → save results.
    """
    master_parsed_path = PARSED_DIR / "ALL_parsed_resumes.json"

    if not master_parsed_path.exists():
        print(f"[ERROR] Parsed resumes file not found: {master_parsed_path}")
        print("        Run resume_parser.py first.")
        return {}

    with open(master_parsed_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    parsed_resumes = data.get("resumes", [])
    print(f"\n[ATS Engine] Loaded {len(parsed_resumes)} parsed resumes.")

    # Score all candidates
    scored = []
    for resume in parsed_resumes:
        engine = ATSScoringEngine(resume)
        result = engine.compute()
        scored.append(result)

    # Rank within each role
    ranked = rank_candidates(scored)

    # Print report to console
    print_ranked_report(ranked)

    # Flatten ranked list
    all_ranked = []
    for role_candidates in ranked.values():
        all_ranked.extend(role_candidates)

    # Overall stats
    shortlisted_count = sum(1 for c in all_ranked if c["shortlisted"])
    avg_score         = round(sum(c["ats_score"] for c in all_ranked) / max(len(all_ranked), 1), 1)

    output = {
        "generated_at":        datetime.now().isoformat(),
        "total_candidates":    len(all_ranked),
        "shortlisted":         shortlisted_count,
        "rejected":            len(all_ranked) - shortlisted_count,
        "average_ats_score":   avg_score,
        "ranked_by_role":      ranked,
        "all_candidates_flat": sorted(all_ranked, key=lambda x: x["ats_score"], reverse=True),
    }

    # Save full report
    out_path = SCORES_DIR / "ATS_scores_ranked.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Save summary CSV-like table
    summary_lines = [
        "rank,resume_id,name,role,ats_score,skills,experience,projects,education,certifications,quality,shortlisted,recommendation"
    ]
    for c in sorted(all_ranked, key=lambda x: x["ats_score"], reverse=True):
        b = c["breakdown"]
        summary_lines.append(
            f"{c['rank']},{c['resume_id']},{c['name']},{c['role_applied']},"
            f"{b['total']},{b['skills_match']},{b['experience']},{b['projects']},"
            f"{b['education']},{b['certifications']},{b['resume_quality']},"
            f"{c['shortlisted']},{c['recommendation'].split('–')[0].strip()}"
        )

    csv_path = SCORES_DIR / "ATS_scores_summary.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))

    print(f"[ATS Engine] ✅ Results saved:")
    print(f"             → {out_path}")
    print(f"             → {csv_path}")
    print(f"\n[SUMMARY] Total: {len(all_ranked)} | Shortlisted: {shortlisted_count} | "
          f"Rejected: {len(all_ranked)-shortlisted_count} | Avg Score: {avg_score}/100\n")

    return output


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_ats_engine()
