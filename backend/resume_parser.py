#!/usr/bin/env python3
"""
=============================================================================
AI-Powered Smart Recruitment System
Phase 3: Resume Parser
=============================================================================
Parses resume JSON files and extracts structured candidate information.
Produces standardized parsed output for the ATS Scoring Engine.
=============================================================================
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

RESUMES_DIR = Path(__file__).parent.parent / "datasets" / "resumes"
PARSED_DIR  = Path(__file__).parent.parent / "datasets" / "parsed_resumes"
PARSED_DIR.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# PARSER CLASS
# ─────────────────────────────────────────────────────────────────────────────

class ResumeParser:
    """
    Parses a candidate resume JSON file and extracts all structured fields
    into a standardised ParsedResume schema for the ATS engine.
    """

    def __init__(self, resume_path: str):
        self.resume_path = Path(resume_path)
        with open(self.resume_path, "r", encoding="utf-8") as f:
            self.raw = json.load(f)

    # ── core extraction methods ────────────────────────────────────────────

    def extract_name(self) -> str:
        return self.raw.get("name", "").strip()

    def extract_email(self) -> str:
        return self.raw.get("email", "").strip().lower()

    def extract_phone(self) -> str:
        phone = self.raw.get("phone", "")
        # Normalise phone — keep digits and leading +
        cleaned = re.sub(r"[^\d+]", "", phone)
        return cleaned

    def extract_linkedin(self) -> Optional[str]:
        return self.raw.get("linkedin", None)

    def extract_github(self) -> Optional[str]:
        return self.raw.get("github", None)

    def extract_portfolio(self) -> Optional[str]:
        return self.raw.get("portfolio", None)

    def extract_address(self) -> str:
        return self.raw.get("address", "").strip()

    def extract_role_applied(self) -> str:
        return self.raw.get("role_applied", "").strip()

    # ── education ─────────────────────────────────────────────────────────

    def extract_education(self) -> list[dict]:
        edu_list = self.raw.get("education", [])
        parsed = []
        for edu in edu_list:
            parsed.append({
                "degree":       edu.get("degree", ""),
                "institution":  edu.get("institution", ""),
                "university":   edu.get("university", ""),
                "cgpa":         edu.get("cgpa", None),
                "cgpa_scale":   edu.get("cgpa_scale", 10.0),
                "year_of_passing": edu.get("year_of_passing", None),
            })
        return parsed

    def extract_highest_degree(self) -> str:
        edu = self.raw.get("education", [])
        if not edu:
            return "Unknown"
        # Return the first degree listed (assumed most recent/highest)
        return edu[0].get("degree", "Unknown")

    def extract_institution(self) -> str:
        edu = self.raw.get("education", [])
        if not edu:
            return "Unknown"
        return edu[0].get("institution", "Unknown")

    def extract_cgpa(self) -> Optional[float]:
        edu = self.raw.get("education", [])
        if not edu:
            return None
        return edu[0].get("cgpa", None)

    # ── experience ────────────────────────────────────────────────────────

    def extract_experience(self) -> list[dict]:
        exp_list = self.raw.get("experience", [])
        parsed = []
        for exp in exp_list:
            parsed.append({
                "company":       exp.get("company", ""),
                "title":         exp.get("title", ""),
                "location":      exp.get("location", ""),
                "type":          exp.get("type", ""),
                "start_date":    exp.get("start_date", ""),
                "end_date":      exp.get("end_date", ""),
                "duration_months": exp.get("duration_months", 0),
                "responsibilities": exp.get("responsibilities", []),
            })
        return parsed

    def extract_years_experience(self) -> float:
        """Sum all full-time and internship months and convert to years."""
        exp_list = self.raw.get("experience", [])
        total_months = 0
        for exp in exp_list:
            exp_type = exp.get("type", "Full-Time")
            months = exp.get("duration_months", 0)
            # Count internships at 50% weight for true experience
            if "Intern" in exp_type:
                total_months += months * 0.5
            elif "Freelance" in exp_type:
                total_months += months * 0.5
            else:
                total_months += months
        return round(total_months / 12, 1)

    def extract_companies(self) -> list[str]:
        return [exp.get("company", "") for exp in self.raw.get("experience", [])]

    # ── skills ────────────────────────────────────────────────────────────

    def extract_skills(self) -> dict:
        return self.raw.get("skills", {})

    def extract_all_skills_flat(self) -> list[str]:
        """Flatten all skill categories into a single deduplicated list."""
        skills = self.raw.get("skills", {})
        flat = []
        for category, items in skills.items():
            if isinstance(items, list):
                flat.extend([s.strip() for s in items if s])
            elif isinstance(items, str):
                flat.append(items.strip())
        return list(dict.fromkeys(flat))  # deduplicate preserving order

    def extract_skill_count(self) -> int:
        return len(self.extract_all_skills_flat())

    # ── projects ──────────────────────────────────────────────────────────

    def extract_projects(self) -> list[dict]:
        return self.raw.get("projects", [])

    def extract_project_count(self) -> int:
        return len(self.raw.get("projects", []))

    # ── certifications ────────────────────────────────────────────────────

    def extract_certifications(self) -> list[dict]:
        return self.raw.get("certifications", [])

    def extract_certification_names(self) -> list[str]:
        return [c.get("name", "") for c in self.raw.get("certifications", [])]

    def extract_certification_count(self) -> int:
        return len(self.raw.get("certifications", []))

    # ── achievements & extras ─────────────────────────────────────────────

    def extract_achievements(self) -> list[str]:
        return self.raw.get("achievements", [])

    def extract_languages(self) -> list[str]:
        return self.raw.get("languages_known", [])

    def extract_soft_skills(self) -> list[str]:
        return self.raw.get("soft_skills", [])

    def extract_interests(self) -> list[str]:
        return self.raw.get("interests", [])

    # ── quality tier & ATS meta ───────────────────────────────────────────

    def extract_quality_tier(self) -> str:
        return self.raw.get("quality_tier", "Unknown")

    # ─────────────────────────────────────────────────────────────────────
    # MAIN PARSE METHOD
    # ─────────────────────────────────────────────────────────────────────

    def parse(self) -> dict:
        """
        Run all extractors and return the full ParsedResume dictionary.
        This is the standard output consumed by the ATS Scoring Engine.
        """
        parsed = {
            # ── identity ──────────────────────────────────────────────────
            "resume_id":        self.raw.get("resume_id", ""),
            "name":             self.extract_name(),
            "email":            self.extract_email(),
            "phone":            self.extract_phone(),
            "linkedin":         self.extract_linkedin(),
            "github":           self.extract_github(),
            "portfolio":        self.extract_portfolio(),
            "address":          self.extract_address(),
            "role_applied":     self.extract_role_applied(),
            "quality_tier":     self.extract_quality_tier(),

            # ── education ─────────────────────────────────────────────────
            "education":        self.extract_education(),
            "highest_degree":   self.extract_highest_degree(),
            "institution":      self.extract_institution(),
            "cgpa":             self.extract_cgpa(),

            # ── experience ────────────────────────────────────────────────
            "experience":       self.extract_experience(),
            "years_experience": self.extract_years_experience(),
            "companies":        self.extract_companies(),

            # ── skills ────────────────────────────────────────────────────
            "skills":           self.extract_skills(),
            "skills_flat":      self.extract_all_skills_flat(),
            "skill_count":      self.extract_skill_count(),

            # ── projects ──────────────────────────────────────────────────
            "projects":         self.extract_projects(),
            "project_count":    self.extract_project_count(),

            # ── certifications ────────────────────────────────────────────
            "certifications":       self.extract_certifications(),
            "certification_names":  self.extract_certification_names(),
            "certification_count":  self.extract_certification_count(),

            # ── extras ────────────────────────────────────────────────────
            "achievements":         self.extract_achievements(),
            "languages_known":      self.extract_languages(),
            "soft_skills":          self.extract_soft_skills(),
            "interests":            self.extract_interests(),

            # ── metadata ──────────────────────────────────────────────────
            "parsed_at":            datetime.now().isoformat(),
            "source_file":          self.resume_path.name,
        }

        return parsed


# ─────────────────────────────────────────────────────────────────────────────
# BATCH PARSER
# ─────────────────────────────────────────────────────────────────────────────

def parse_all_resumes(resumes_dir: Path = RESUMES_DIR,
                      output_dir: Path = PARSED_DIR) -> list[dict]:
    """
    Parse all resume JSON files in resumes_dir.
    Saves each parsed resume to output_dir and returns the full list.
    """
    resume_files = sorted([
        f for f in resumes_dir.glob("*.json")
        if f.name != "MASTER_candidates_index.json"
    ])

    if not resume_files:
        print(f"[ERROR] No resume JSON files found in: {resumes_dir}")
        return []

    all_parsed = []
    print(f"\n{'='*60}")
    print(f"  RESUME PARSER — AI Recruitment System")
    print(f"{'='*60}")
    print(f"  Found {len(resume_files)} resume(s) to parse.\n")

    for i, fpath in enumerate(resume_files, 1):
        try:
            parser = ResumeParser(str(fpath))
            parsed = parser.parse()

            # Save individual parsed file
            out_path = output_dir / f"PARSED_{fpath.name}"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(parsed, f, indent=2, ensure_ascii=False)

            print(f"  [{i:02d}] ✅  {parsed['name']:<22} | {parsed['role_applied']:<26} | "
                  f"Exp: {parsed['years_experience']} yrs | "
                  f"Skills: {parsed['skill_count']} | "
                  f"Certs: {parsed['certification_count']}")

            all_parsed.append(parsed)

        except Exception as e:
            print(f"  [{i:02d}] ❌  ERROR parsing {fpath.name}: {e}")

    # Save master parsed output
    master_path = output_dir / "ALL_parsed_resumes.json"
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump({
            "total": len(all_parsed),
            "parsed_at": datetime.now().isoformat(),
            "resumes": all_parsed
        }, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"  ✅  Parsing complete.")
    print(f"  📁  Parsed files saved to: {output_dir}")
    print(f"  📊  Total parsed: {len(all_parsed)} / {len(resume_files)}")
    print(f"{'='*60}\n")

    return all_parsed


# ─────────────────────────────────────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Single file mode: python resume_parser.py path/to/resume.json
        path = sys.argv[1]
        parser = ResumeParser(path)
        result = parser.parse()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Batch mode: parse all resumes
        parse_all_resumes()
