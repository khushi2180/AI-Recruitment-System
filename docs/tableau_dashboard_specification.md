# TalentAI — Tableau Dashboard Specification
## AI-Powered Smart Recruitment System
### Phase 11: Data Visualisation & BI Dashboard Design

---

## OVERVIEW

This document specifies the complete Tableau dashboard design for the TalentAI recruitment system.  
The dashboards connect directly to `reports/ats_scores/ATS_scores_summary.csv` and  
`reports/bias_analysis/bias_analysis_results.json` as live data sources.

**Total Dashboards:** 5  
**Total Worksheets:** 18  
**Data Source:** CSV + JSON exports from the Python backend pipeline

---

## DATA SOURCE SETUP IN TABLEAU

### Primary Data Source: ATS Scores CSV
```
File:    reports/ats_scores/ATS_scores_summary.csv
Type:    Flat file (CSV)
Fields:
  rank              (integer)
  resume_id         (string / dimension)
  name              (string / dimension)
  role              (string / dimension — 5 values)
  ats_score         (float / measure)
  skills            (float / measure)
  experience        (float / measure)
  projects          (float / measure)
  education         (float / measure)
  certifications    (float / measure)
  quality           (float / measure)
  shortlisted       (boolean → dimension: TRUE/FALSE)
  recommendation    (string / dimension)

Calculated Fields to Create:
  [Score Bucket]:
    IF [ats_score] >= 90 THEN "90–100 (Excellent)"
    ELSEIF [ats_score] >= 80 THEN "80–89 (Strong)"
    ELSEIF [ats_score] >= 70 THEN "70–79 (Good)"
    ELSEIF [ats_score] >= 60 THEN "60–69 (Average)"
    ELSEIF [ats_score] >= 40 THEN "40–59 (Weak)"
    ELSE "0–39 (Poor)" END

  [Status Label]:
    IF [shortlisted] = TRUE THEN "✅ Shortlisted" ELSE "❌ Rejected" END

  [Score Color]:
    IF [ats_score] >= 80 THEN "High"
    ELSEIF [ats_score] >= 65 THEN "Medium"
    ELSE "Low" END
```

### Secondary Data Source: Master Candidates Index
```
File:    datasets/resumes/MASTER_candidates_index.json
Fields (after JSON flattening):
  resume_id, name, role, tier, ats_score, rank,
  shortlisted, experience_years, cgpa, institution
```

---

## DASHBOARD 1: EXECUTIVE RECRUITMENT SUMMARY

**Size:** 1400 × 900px | **Layout:** Tiled

### Worksheets Included:

#### 1A — KPI Summary Numbers (Big Number Tiles)
```
Type:     Text table (formatted as large numbers)
Metrics:  Total Applications: 30
          Shortlisted:        19 (63.3%)
          Avg ATS Score:      67.2
          Rejection Rate:     36.7%

Formatting:
  Values:  Space Grotesk font equivalent, 48px
  Labels:  11px, grey, uppercase
  Colors:  Purple / Green / Amber / Red per metric
```

#### 1B — Applications by Role (Horizontal Bar Chart)
```
Rows:     Role (Software Engineer, Cyber Security, Data Analyst, Product Manager, UI/UX)
Cols:     COUNT([name])
Color:    [shortlisted] — Blue=Shortlisted, Red=Rejected (stacked)
Sort:     By total applications (desc)
Label:    Show count inside each bar segment

Filters:  Shortlisted (All / Yes / No)
```

#### 1C — ATS Score Distribution (Histogram)
```
Type:     Histogram / Bar chart on [Score Bucket]
X-axis:   Score Bucket (6 bins)
Y-axis:   Number of candidates
Color:    Low=Red, Medium=Amber, High=Green (categorical)
Annotation: Add reference line at score=65 (shortlist threshold) — dashed red
```

#### 1D — Shortlisted vs Rejected Donut (Pie Chart)
```
Type:     Pie chart
Marks:    [Status Label] as color + label
Size:     Fixed 220×220px
Labels:   Show % + count
Colors:   Shortlisted: #8B5CF6 | Rejected: #EF4444
```

#### 1E — Average Score by Role (Grouped Bar)
```
Cols:     Role
Rows:     AVG([ats_score])
Color:    [shortlisted] (segmented: shortlisted avg vs rejected avg)
Show:     Reference line at 65 (shortlist threshold)
Tooltip:  Count, avg score, shortlist rate
```

**Dashboard 1 Filters (Global):**
- Role selector (all / individual)
- Shortlisted / All
- Score range slider

---

## DASHBOARD 2: CANDIDATE RANKING DEEP-DIVE

**Size:** 1400 × 1000px | **Layout:** Tiled

#### 2A — Full Candidate Ranking Table
```
Rows:     [rank] | [name] | [role] | [ats_score] | [skills] | [experience] |
          [projects] | [education] | [certifications] | [quality] | [shortlisted]
Sort:     ATS score descending (default)
Color:    Row shading by [Score Color]: Green/Amber/Red
Sparkbar: Show inline bar for [ats_score] column (0–100 scale)
Filters:  Role dropdown | Min score filter | Shortlisted checkbox

Conditional Formatting:
  ats_score ≥ 80: cell background green-tint
  ats_score 60–79: amber-tint
  ats_score < 60:  red-tint
```

#### 2B — Score Component Stacked Bar (Per Candidate)
```
Type:     Stacked horizontal bar
Rows:     [name] (top 15 by score)
Cols:     [skills] + [experience] + [projects] + [education] + [certifications] + [quality]
Colors:   Each component a different hue (6 colors from chart palette)
Max:      100 (total bar width)
Show:     Component labels on segments ≥ 4 units wide
Tooltip:  Full breakdown

Purpose:  Instantly shows WHERE candidates are strong/weak
```

#### 2C — Scatter Plot: Experience vs ATS Score
```
X-axis:   [experience_years] (0–6)
Y-axis:   [ats_score] (0–100)
Color:    [role]
Size:     [skill_count] (relative)
Labels:   Show [name] on hover
Reference Lines:
  X: 2 years (entry-level threshold)
  Y: 65 (shortlist threshold)
  Creates 4 quadrants:
    Top-Right: High exp + High score → Prime candidates
    Top-Left:  Low exp + High score  → High-potential juniors
    Bottom-Right: High exp + Low score → Overqualified mismatch
    Bottom-Left:  Low exp + Low score  → Reject zone
```

#### 2D — CGPA vs ATS Score Scatter
```
Similar to 2C but:
X-axis:   [cgpa] (5.0–10.0)
Y-axis:   [ats_score]
Color:    [tier] (Excellent/Average/Poor)
Purpose:  Visualise correlation between academic performance and ATS score
```

---

## DASHBOARD 3: HIRING FUNNEL ANALYTICS

**Size:** 1400 × 900px | **Layout:** Tiled

#### 3A — Stage-by-Stage Funnel (Funnel Chart)
```
Type:     Custom funnel (bar chart formatted as trapezoid funnel)
Stages:
  Applications Received: 30
  Resumes Parsed:        30
  ATS Screened (≥55):    22
  Shortlisted (≥65):     19
  HR Call:               16
  Technical Interview:   14
  Panel Interview:       10
  Offers Sent:            8
  Offers Accepted:        6
  Joiners (Day 1):        5

Color:    Gradient dark-purple → light-purple top to bottom
Labels:   Stage name + count + conversion % from previous
```

#### 3B — Conversion Rate by Stage (Line Chart)
```
X-axis:   Stage (ordered 1–10)
Y-axis:   Cumulative conversion % from applications
Line:     Smooth, purple, with data point markers
Shading:  Area below line, purple gradient
Annotations: Mark each drop with the reason (tooltip)
```

#### 3C — Per-Role Funnel Comparison (Grouped Bar)
```
Cols:     Stage (Applied → Shortlisted → Interviewed → Offered → Joined)
Rows:     Count
Color:    Role (5 colors)
Type:     Grouped bar (each role has its own bar per stage)
Filter:   Role selector
```

#### 3D — Time-to-Hire Gauge
```
Type:     Gauge chart (custom — using pie chart trick)
Value:    18 days
Target:   21 days (industry benchmark)
Color:    Green (under target)
Label:    "18 days avg · 3 days under benchmark"
```

#### 3E — Offer Acceptance Rate Comparison
```
Type:     Bar chart with benchmark reference line
Y-axis:   Acceptance rate %
Bars:     Our system (75%) | Industry benchmark (68%)
Color:    Our bar: Purple | Benchmark: Grey dashed line
Label:    +7% above benchmark
```

---

## DASHBOARD 4: BIAS & DIVERSITY ANALYTICS

**Size:** 1400 × 1000px | **Layout:** Tiled

#### 4A — Gender Distribution by Role (Stacked Bar)
```
Rows:     Role
Cols:     COUNT([name])
Color:    Gender (Female: Pink #EC4899 | Male: Blue #3B82F6)
Type:     100% stacked bar (shows proportion)
Tooltip:  Gender count, shortlist rate by gender
Target:   Reference line at 50% (parity goal)
```

#### 4B — Shortlist Rate by Gender (Grouped Bar)
```
Cols:     Gender
Rows:     SUM(shortlisted) / COUNT(total) per gender
Color:    Purple gradient
Labels:   Percentage on each bar
```

#### 4C — Institution Tier Score Comparison (Box Plot)
```
Type:     Box & Whisker plot
X-axis:   Institution Tier (Tier-1, Tier-2, Tier-3)
Y-axis:   [ats_score]
Color:    Tier (Green=T1, Amber=T2, Red=T3)
Annotations:
  Mark: Tier-1 avg = 79.3 | Tier-3 avg = 54.1 | Gap: 25.2 pts
Purpose: Visually demonstrates institution bias
```

#### 4D — Bias Severity Heatmap
```
Type:     Text table with color encoding (manual data entry)
Rows:     Bias Dimension (10 total)
Cols:     Severity (HIGH / MEDIUM / LOW / UNOBSERVABLE)
Values:   Score gap where applicable
Color:    HIGH=Red | MEDIUM=Amber | LOW=Green | UNOBS=Grey
Cell size: Fixed, large text for easy reading
```

#### 4E — Score Gap by Dimension (Horizontal Bar)
```
Type:     Horizontal bar chart
Rows:     Bias Dimension (only quantifiable ones — 8)
Cols:     Score gap (positive = disadvantaged group scores lower)
Color:    Gap size → Red gradient (larger = darker red)
Reference line: 5 points (LOW threshold)
Reference line: 15 points (HIGH threshold)
Sort:     Descending by gap size
```

#### 4F — Diversity Index Score (Big Number)
```
Type:     Text / number display
Metric:   Composite score: (Female % × 0.4) + (Tier-3 shortlist rate × 0.3) + (CGPA < 7 shortlisted ÷ total × 0.3)
Display:  Large number 0–100
Color:    Red if <50, Amber if 50–70, Green if >70
Label:    "TalentAI Diversity Index — Summer 2024"
```

#### 4G — Recommendations Summary Table
```
Type:     Text table
Rows:     Each bias dimension (HIGH ones first)
Cols:     Dimension | Severity | Top Recommendation | Owner | Timeline
Purpose:  Action plan visible to HR leadership
```

---

## DASHBOARD 5: AI PERFORMANCE ANALYTICS

**Size:** 1400 × 900px | **Layout:** Tiled

#### 5A — AI vs Manual Screening Comparison
```
Type:     Grouped bar
Metrics:  Time to screen (AI: 0.8s vs Manual: 8+ hours)
          Consistency score (AI: 100% vs Manual: ~72% inter-rater)
          Bias dimensions monitored (AI: 10 vs Manual: ~2)
          Cost per screening (AI: ₹2 vs Manual: ₹800)
Purpose:  Quantifies AI ROI for presentation
```

#### 5B — Score Consistency by Role (Box Plot)
```
Type:     Box plot
X-axis:   Role
Y-axis:   ATS score variance within role
Shows:    How spread the scores are within each role pool
Insight:  Low variance = consistent scoring → AI reliability
```

#### 5C — Recommendation Accuracy Projection
```
Type:     Stacked area chart (simulated over 12 months)
X-axis:   Month (Jan–Dec 2024, projected)
Y-axis:   Predicted hire quality score
Lines:    AI-screened hires vs Manual-screened (historical)
Legend:   AI Pipeline | Traditional Pipeline
Note:     Annotate as "Projected — based on ATS correlation to performance"
```

#### 5D — Key AI Metrics Summary
```
Type:     KPI tiles (4 tiles)
Metrics:
  Resumes Parsed:           30 in 0.8 seconds
  Skills Matched:           35% weight — most decisive factor
  Bias Dimensions Checked:  10 (4 HIGH, 2 MEDIUM)
  Estimated Time Saved:     34.5 hours vs manual screening
```

---

## TABLEAU FORMATTING STANDARDS

### Color Palette (Match Dashboard)
```
Role Colors:
  Software Engineer:       #8B5CF6 (Purple)
  Cyber Security Analyst:  #EF4444 (Red)
  Data Analyst:            #F59E0B (Amber)
  Product Manager:         #3B82F6 (Blue)
  UI/UX Designer:          #EC4899 (Pink)

Background:   #1A1A28 (dark card)
Grid lines:   rgba(139,92,246,0.15)
Text:         #F8FAFC (primary), #94A3B8 (secondary)
```

### Typography in Tableau
```
Dashboard title:  Tableau Semibold, 18pt, white
Worksheet title:  Tableau Book, 14pt, #C4B5FD (light purple)
Axis labels:      Tableau Light, 10pt, #94A3B8
Data labels:      Tableau Semibold, 10–11pt, white
Tooltips:         Tableau Book, 11pt
```

### Tooltip Template (all charts)
```
<b><Candidate Name></b>
Role: <Role>
ATS Score: <Score> / 100
Status: <Status Label>
─────────────────
Skills: <skills>/35 | Exp: <experience>/25
Projects: <projects>/15 | Edu: <education>/10
```

### Dashboard Actions
```
Filter Action:  Click role on any chart → filter all worksheets on that dashboard
Highlight:      Hover on name → highlight across all charts
URL Action:     Click candidate → open candidate profile URL (future)
```

---

## DATA REFRESH SCHEDULE

```
Development:   Manual refresh after each Python pipeline run
Production:    Tableau Server → scheduled refresh every 24 hours
Alert:         If avg score drops >5pts from previous day → email alert to recruiter
```

---

## TABLEAU PUBLIC / EXPORT

To share this dashboard:
1. File → Save to Tableau Public
2. URL format: `public.tableau.com/app/profile/[username]/viz/TalentAI-Recruitment`
3. Embed in documentation as iframe
4. Export PDF: Dashboard → Export → Image / PDF for presentation slides

---

*TalentAI — Tableau Dashboard Specification v1.0*  
*AI-Powered Smart Recruitment System — Capstone Project 2024*
