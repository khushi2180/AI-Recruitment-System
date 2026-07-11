import os
import json
import re
import io
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Load .env file
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from google import genai
from groq import Groq
import pdfplumber
from flask import Flask

app = Flask(__name__)
# ─── Config ───────────────────────────────────────────────────────────────────
RESUMES_DIR = Path(__file__).parent / "datasets" / "resumes"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")

# Primary AI: Gemini
if GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    GEMINI_MODEL = "gemini-2.0-flash-lite"
    print(f"[CV Analysis] Gemini AI loaded ✓ (model: {GEMINI_MODEL})")
else:
    gemini_client = None
    GEMINI_MODEL = None
    print("[CV Analysis] WARNING: No GEMINI_API_KEY found in .env")

# Fallback AI: Groq (Llama 3.3 70B — free tier: 14,400 req/day)
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
    GROQ_MODEL = "llama-3.3-70b-versatile"
    print(f"[CV Analysis] Groq fallback loaded ✓ (model: {GROQ_MODEL})")
else:
    groq_client = None
    GROQ_MODEL = None
    print("[CV Analysis] INFO: No GROQ_API_KEY — Groq fallback unavailable.")


def call_ai(prompt: str) -> tuple[str, str]:
    """
    Call Gemini first. If quota is exhausted (429), automatically fall back to Groq.
    Returns (response_text, provider_used) where provider_used is 'gemini' or 'groq'.
    Raises RuntimeError if both fail.
    """
    # ── Try Gemini ──────────────────────────────────────────────────────────
    if gemini_client:
        try:
            resp = gemini_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            return resp.text.strip(), "gemini"
        except Exception as e:
            err = str(e)
            if '429' in err or 'RESOURCE_EXHAUSTED' in err:
                print("[CV Analysis] Gemini quota exhausted → switching to Groq fallback")
                # Fall through to Groq below
            else:
                raise RuntimeError(f"Gemini API error: {err[:200]}")

    # ── Try Groq fallback ───────────────────────────────────────────────────
    if groq_client:
        try:
            resp = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=4096,
            )
            return resp.choices[0].message.content.strip(), "groq"
        except Exception as e:
            raise RuntimeError(f"Groq API error: {str(e)[:200]}")

    raise RuntimeError("No AI provider available. Add GEMINI_API_KEY or GROQ_API_KEY to .env")

# ─── Role prefix mapping ───────────────────────────────────────────────────────
ROLE_PREFIXES = {
    "software engineer":      "SE",
    "cyber security analyst": "CSA",
    "cybersecurity analyst":  "CSA",
    "data analyst":           "DA",
    "data scientist":         "DA",
    "product manager":        "PM",
    "ui/ux designer":         "UX",
    "ux designer":            "UX",
    "ui designer":            "UX",
}

def get_role_prefix(role: str) -> str:
    role_lower = role.lower().strip()
    for key, prefix in ROLE_PREFIXES.items():
        if key in role_lower:
            return prefix
    return "".join(w[0].upper() for w in role.split() if w) or "GEN"

def get_next_index(prefix: str) -> int:
    pattern = re.compile(rf"^{re.escape(prefix)}_(\d+)_", re.IGNORECASE)
    max_idx = 0
    for fname in os.listdir(RESUMES_DIR):
        m = pattern.match(fname)
        if m:
            idx = int(m.group(1))
            if idx > max_idx:
                max_idx = idx
    return max_idx + 1

# ─── Gemini Resume Parser Prompt ──────────────────────────────────────────────
RESUME_PARSE_PROMPT = """You are an expert resume parser for a recruitment system.

══════════════════════════════════════════════════════
STRICT RULES — READ CAREFULLY BEFORE PARSING:
══════════════════════════════════════════════════════

RULE 1 — ONLY EXTRACT, NEVER INVENT:
  - Extract ONLY information that is explicitly written in the resume text.
  - If a field is not present in the resume, use "" (empty string) or [] (empty array) or 0.
  - Do NOT infer, guess, assume, or generate any data not directly stated in the resume.
  - Do NOT use the examples in this prompt as actual output values.

RULE 2 — EDUCATION vs EXPERIENCE ARE COMPLETELY SEPARATE:
  - "education" section = degrees, colleges, universities, CGPA, graduation year only.
  - "experience" section = jobs, internships, freelance work at real companies/organisations.
  - A college or university is NEVER a company in the experience section.
  - Education years (e.g., "2019–2023") are graduation years, NOT work experience duration.
  - CGPA, year_of_passing, degree name → go in "education" ONLY, never in "experience".

RULE 3 — EXPERIENCE DURATION (calculate carefully):
  - duration_months = count actual calendar months between start_date and end_date.
  - Examples:
      "Jun 2023 – Dec 2023" → 6 months → duration_months: 6
      "Jan 2022 – Jun 2023" → 17 months → duration_months: 17
      "Mar 2024 – Present"  → calculate from Mar 2024 to approx Jul 2025 → ~16 months
      "6 months internship" → duration_months: 6
  - experience_years = (sum of all duration_months across ALL jobs) / 12, rounded to 2 decimal places.
      8 months  → experience_years: 0.67
      6 months  → experience_years: 0.50
      18 months → experience_years: 1.50
      0 months  → experience_years: 0.00
  - NEVER use graduation year or college year gaps to calculate experience_years.

RULE 4 — SKILLS:
  - List ONLY skills explicitly written in the resume.
  - Group them into meaningful categories (e.g., "languages", "frameworks", "tools", "databases", "cloud").
  - Do NOT add skills that are not in the resume text.

RULE 5 — PROJECTS:
  - List ONLY projects explicitly mentioned in the resume.
  - tech_stack = ONLY technologies explicitly listed for THAT specific project.
  - description = copy the description as written, do not paraphrase or expand.

RULE 6 — CERTIFICATIONS:
  - List ONLY certifications explicitly stated in the resume.
  - If issuer or year is not stated, use "" or 0 respectively.
  - Do NOT fabricate or guess certification names, issuers, or years.

RULE 7 — ATS SCORE (score ONLY based on resume content):
  - skills_match (0–30): more diverse and relevant skills = higher score
  - experience (0–20): based on total duration_months of WORK experience ONLY (not education):
      0 months  = 0 pts
      1–6 months = 5 pts
      7–12 months = 10 pts
      13–24 months = 15 pts
      25+ months = 20 pts
  - projects (0–15): number and relevance of projects listed
  - education (0–10): degree level, CGPA (only if stated in resume)
  - certifications (0–15): number and relevance of certifications listed
  - resume_quality (0–10): overall completeness and clarity
  - total = sum of all above
  - shortlisted = true if total >= 65
  - quality_tier = "Excellent" if total >= 80, "Average" if total >= 55, else "Poor"

══════════════════════════════════════════════════════
OUTPUT — Return EXACTLY this JSON schema (no extras):
══════════════════════════════════════════════════════

{
  "name": "full name as written in resume",
  "email": "email or empty string",
  "phone": "phone or empty string",
  "linkedin": "linkedin URL or empty string",
  "github": "github URL or empty string",
  "portfolio": "portfolio URL or empty string",
  "address": "city or address if stated, else empty string",
  "role_applied": "ONE of: Software Engineer | Cyber Security Analyst | Data Analyst | Product Manager | UI/UX Designer — infer from resume job titles and skills",
  "quality_tier": "Excellent | Average | Poor",
  "summary": "professional summary section exactly as written in resume, or empty string if absent",
  "education": [
    {
      "degree": "exact degree name as written",
      "institution": "exact college or university name",
      "university": "parent university name if stated, else empty string",
      "cgpa": 0.0,
      "cgpa_scale": 10.0,
      "year_of_passing": 0,
      "relevant_courses": ["only courses explicitly listed in resume"]
    }
  ],
  "experience": [
    {
      "company": "company or organisation name (MUST be a real employer, never a college)",
      "title": "exact job title as written",
      "location": "location if stated, else empty string",
      "type": "Full-Time | Internship | Part-Time | Freelance | Contract",
      "start_date": "Mon YYYY or YYYY",
      "end_date": "Mon YYYY or Present",
      "duration_months": 0,
      "responsibilities": ["exact bullet points from resume — copy verbatim, do not paraphrase"]
    }
  ],
  "skills": {
    "category_name": ["skill1", "skill2"]
  },
  "projects": [
    {
      "name": "exact project name as written",
      "tech_stack": ["only technologies explicitly listed for this project"],
      "description": "description exactly as written in resume",
      "github_link": "URL if stated, else empty string"
    }
  ],
  "certifications": [
    {
      "name": "exact certification name as written",
      "issuer": "issuer if stated, else empty string",
      "year": 0
    }
  ],
  "achievements": ["exact achievements as written in resume"],
  "languages_known": ["only languages explicitly listed"],
  "soft_skills": ["only soft skills explicitly listed"],
  "interests": ["only interests explicitly listed"],
  "experience_years": 0.0,
  "ats_score": {
    "total": 0,
    "breakdown": {
      "skills_match": 0,
      "experience": 0,
      "projects": 0,
      "education": 0,
      "certifications": 0,
      "resume_quality": 0
    },
    "shortlisted": false
  }
}

══════════════════════════════════════════════════════
RESUME TEXT (parse from THIS text ONLY — do not invent):
══════════════════════════════════════════════════════
{resume_text}

IMPORTANT: Return ONLY the raw JSON object above. No markdown. No ```json fences. No explanation text."""

# ─── Gemini Question Generator Prompt ─────────────────────────────────────────
QUESTIONS_PROMPT = """You are an expert technical recruiter for a top tech company.

Generate exactly 13 tailored interview questions for a candidate with the following profile:
- Role: {role}
- Candidate Name: {name}
- Key Skills: {skills}
- Tier: {tier}
- Experience: {exp} years

Return a JSON object in this exact format:
{{
  "technical": [
    {{"q": "question text", "difficulty": "Easy|Medium|Hard", "topic": "topic name"}},
    {{"q": "question text", "difficulty": "Easy|Medium|Hard", "topic": "topic name"}},
    {{"q": "question text", "difficulty": "Easy|Medium|Hard", "topic": "topic name"}},
    {{"q": "question text", "difficulty": "Easy|Medium|Hard", "topic": "topic name"}},
    {{"q": "question text", "difficulty": "Easy|Medium|Hard", "topic": "topic name"}}
  ],
  "behavioural": [
    {{"q": "question text", "focus": "focus area"}},
    {{"q": "question text", "focus": "focus area"}},
    {{"q": "question text", "focus": "focus area"}},
    {{"q": "question text", "focus": "focus area"}},
    {{"q": "question text", "focus": "focus area"}}
  ],
  "situational": [
    {{"q": "question text", "scenario": "scenario type"}},
    {{"q": "question text", "scenario": "scenario type"}},
    {{"q": "question text", "scenario": "scenario type"}}
  ]
}}

Make technical questions specific to the candidate's listed skills and role.
Make behavioural questions relevant to their experience level.
Return ONLY the JSON object. No markdown. No explanation."""

# ─── HTTP Request Handler ──────────────────────────────────────────────────────
class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default access logs

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        try:
            if self.path == '/api/list_resumes':
                resumes = []
                for f in RESUMES_DIR.glob('*.json'):
                    try:
                        with open(f, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            # Ensure it's a valid candidate JSON by checking for ats_score
                            if 'ats_score' in data:
                                resumes.append(data)
                    except Exception as e:
                        print(f"Skipping {f.name}: {e}")
                
                self.send_json({"status": "success", "count": len(resumes), "resumes": resumes})
                return
                
            # If path not handled
            self.send_response(404)
            self.end_headers()
        except Exception as e:
            self.send_json({"status": "error", "message": str(e)}, 500)

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(body)

    def read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(length).decode('utf-8'))

    def do_POST(self):
        try:
            # ── /api/extract_pdf_text ─────────────────────────────────────────
            # Receives raw PDF bytes, returns clean extracted text via pdfplumber
            if self.path == '/api/extract_pdf_text':
                length = int(self.headers.get('Content-Length', 0))
                pdf_bytes = self.rfile.read(length)

                if not pdf_bytes:
                    self.send_json({"status": "error", "message": "No PDF data received"}, 400)
                    return

                try:
                    text_pages = []
                    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                        for page in pdf.pages:
                            # extract_text(layout=True) preserves column structure
                            page_text = page.extract_text(layout=True)
                            if page_text:
                                text_pages.append(page_text.strip())

                    full_text = "\n\n".join(text_pages)

                    if not full_text.strip():
                        self.send_json({"status": "error", "message": "No readable text found. The PDF may be scanned/image-based."}, 422)
                        return

                    print(f"[pdfplumber] Extracted {len(full_text)} chars from PDF")
                    self.send_json({"status": "success", "text": full_text, "chars": len(full_text)})
                    return

                except Exception as e:
                    self.send_json({"status": "error", "message": f"PDF extraction error: {str(e)[:200]}"}, 500)
                    return

            data = self.read_body()

            # ── /api/parse_resume_with_gemini ────────────────────────────────
            if self.path == '/api/parse_resume_with_gemini':
                resume_text = data.get("text", "").strip()
                filename_name = data.get("name", "Candidate")

                if not resume_text:
                    self.send_json({"status": "error", "message": "No text provided"}, 400)
                    return

                if not gemini_client and not groq_client:
                    self.send_json({"status": "error", "message": "No AI configured. Add GEMINI_API_KEY or GROQ_API_KEY to .env"}, 503)
                    return

                prompt = RESUME_PARSE_PROMPT.replace("{resume_text}", resume_text[:10000])

                try:
                    raw, provider = call_ai(prompt)
                except RuntimeError as ai_err:
                    self.send_json({"status": "error", "message": str(ai_err)}, 502)
                    return

                raw = re.sub(r'^```(?:json)?\s*', '', raw)
                raw = re.sub(r'\s*```$', '', raw)

                try:
                    parsed = json.loads(raw)
                except json.JSONDecodeError:
                    self.send_json({"status": "error", "message": f"AI ({provider}) returned non-JSON output. Try again."}, 500)
                    return

                if not parsed.get("name") or parsed["name"] in ("", "Candidate", "full name as written in resume"):
                    parsed["name"] = filename_name

                print(f"[{provider.upper()}] Parsed: {parsed.get('name')} | {parsed.get('role_applied')} | ATS={parsed.get('ats_score', {}).get('total', '?')} | Exp={parsed.get('experience_years', '?')}y")
                self.send_json({"status": "success", "parsed": parsed, "provider": provider})

            # ── /api/save_resume ─────────────────────────────────────────────
            elif self.path == '/api/save_resume':
                role = data.get("role_applied", "Unknown")
                name = data.get("name", "Candidate")
                prefix = get_role_prefix(role)
                idx = get_next_index(prefix)
                name_part = name.replace(" ", "_")
                filename = f"{prefix}_{idx:03d}_{name_part}.json"
                filepath = RESUMES_DIR / filename
                data["resume_id"] = f"{prefix}-{idx:03d}"

                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                print(f"[CV Analysis] Saved: {filename}")
                self.send_json({"status": "success", "filepath": str(filepath), "filename": filename, "resume_id": data["resume_id"]})

            # ── /api/delete_resume ───────────────────────────────────────────
            elif self.path == '/api/delete_resume':
                name = data.get("name", "")
                name_clean = re.sub(r"[^a-z]", "", name.lower())
                deleted_file = None

                for f in os.listdir(RESUMES_DIR):
                    file_clean = re.sub(r"[^a-z]", "", f.lower())
                    if name_clean and name_clean in file_clean:
                        fp = RESUMES_DIR / f
                        if fp.exists():
                            fp.unlink()
                            deleted_file = f
                            print(f"[CV Analysis] Deleted: {f}")
                            break

                self.send_json({"status": "success", "filepath": str(RESUMES_DIR / deleted_file) if deleted_file else None, "filename": deleted_file})

            # ── /api/generate_questions ──────────────────────────────────────
            elif self.path == '/api/generate_questions':
                role   = data.get("role", "Software Engineer")
                name   = data.get("name", "the candidate")
                skills = ", ".join(data.get("skills", [])) or "general skills"
                tier   = data.get("tier", "Average")
                exp    = data.get("exp", 0)

                if not gemini_client and not groq_client:
                    self.send_json({"status": "error", "message": "No AI configured. Add GEMINI_API_KEY or GROQ_API_KEY to .env"}, 503)
                    return

                prompt = QUESTIONS_PROMPT.format(role=role, name=name, skills=skills, tier=tier, exp=exp)

                try:
                    raw, provider = call_ai(prompt)
                except RuntimeError as ai_err:
                    self.send_json({"status": "error", "message": str(ai_err)}, 502)
                    return

                raw = re.sub(r'^```(?:json)?\s*', '', raw)
                raw = re.sub(r'\s*```$', '', raw)

                try:
                    questions = json.loads(raw)
                except json.JSONDecodeError:
                    self.send_json({"status": "error", "message": f"AI ({provider}) returned non-JSON for questions. Try again."}, 500)
                    return

                print(f"[{provider.upper()}] Generated questions for {role}")
                self.send_json({"status": "success", "questions": questions, "provider": provider})

            else:
                self.send_response(404)
                self.end_headers()

        except json.JSONDecodeError as e:
            print(f"[JSON Error] {e}")
            self.send_json({"status": "error", "message": f"JSON parse error: {str(e)}"}, 500)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_json({"status": "error", "message": str(e)}, 500)


def run(port=5001):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    gemini_status = '✓ Connected' if gemini_client else '✗ Not configured'
    groq_status   = '✓ Connected' if groq_client   else '✗ Not configured'
    print(f"╔══════════════════════════════════════════════════╗")
    print(f"║  CV Analysis Server  —  http://localhost:{port}       ║")
    print(f"║  Gemini  (primary):  {gemini_status:<28}║")
    print(f"║  Groq    (fallback): {groq_status:<28}║")
    print(f"╚══════════════════════════════════════════════════╝")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
