# PRD — SIH PPT Score Checker ("SIH-ATS")

## 1. One-line pitch
An "ATS-style" scanner for Smart India Hackathon idea presentations — teams upload their PPT/PDF, get an instant, evidence-backed score against the *actual* current-year official SIH rubric, plus line-by-line fixes, before they submit to the real portal.

## 2. Problem
- ~50,000+ teams submit SIH idea PPTs every cycle. Evaluators spend 2–3 minutes per deck.
- Teams have no way to check, before submitting, whether their deck follows the current official format (slide count, required sections, file type) or whether their content is actually strong (on-topic, technically specific, not generic buzzwords).
- The official format changes almost every year (slide count, sections, submission file type), so static "template" blogs and PPT downloads go stale fast and give false confidence.
- No existing tool (ATS checkers are resume-only) scores a hackathon idea deck against hackathon-specific criteria.

## 3. Target users
- **Primary**: SIH participants (engineering students, Tier 2/3 colleges especially — high volume, high anxiety, price-sensitive).
- **Secondary**: College SIH nodal cells / SPOCs who screen hundreds of internal submissions before forwarding to the national portal — potential B2B angle later (bulk screening dashboard).
- **Tertiary**: Faculty mentors guiding multiple teams.

## 4. Goals (MVP)
1. Let a user upload a PPTX or PDF and get a score in under 60 seconds.
2. Score must be **explainable** — every point lost has a stated reason, ideally citing the official doc.
3. Score reflects the **current year's actual official rubric**, not a generic hackathon template.
4. Free tier gets people in the door; paid tier unlocks unlimited checks + rewrite suggestions + before/after diffing.

## 5. Non-goals (explicitly out of MVP scope)
- No live "grand finale" pitch/speech scoring (voice, delivery) — PPT/PDF content only.
- No auto-generation of a full deck from scratch (may become a V2 feature, but MVP is *scoring*, not *authoring*).
- No claim of being an "official" SIH tool or affiliation with AICTE/MoE — must be clearly disclaimed everywhere (legal risk otherwise).
- No fully automatic self-training model at launch (see `tech-architecture.md` — feedback loop is human-in-the-loop, not autonomous).

## 6. Core features

### 6.1 Upload & Score (core loop)
- Upload `.pptx` or `.pdf` (max size per current official limit, currently ~25MB from institute portals, PDF preferred).
- Select the team's Problem Statement from a searchable dropdown (scraped/hosted PS bank) — this powers alignment scoring.
- Async processing with a visible progress indicator.
- Output: overall score /100, category breakdown, slide-by-slide flags, and specific rewrite suggestions.

### 6.2 Scoring categories (see `rubric-spec.md` for full detail and current weights)
- Structure & Format compliance (rule-based)
- Problem Statement alignment (embeddings)
- Technical depth (LLM-assisted)
- Originality / overlap with past decks (embeddings against corpus)
- Presentation clarity (rule-based: text density, diagrams vs text, font size)

### 6.3 Report page
- Big overall score, color-coded category cards, expandable per-slide feedback.
- Every deduction shows a "why" — ideally with a citation back to the official format doc excerpt.
- Downloadable/shareable report (PDF export or shareable link).

### 6.4 Re-check & diff
- Paid users can re-upload after edits and see a score delta ("64 → 81, +17") with what specifically improved.

### 6.5 Rubric freshness
- Every report is stamped with the rubric version used (e.g. "Scored against SIH2026 official format, published [date]").
- Admin-side alert when a new official doc is detected so the rubric can be reviewed and versioned (see `tech-architecture.md`).

### 6.6 Accounts & monetization
- Auth (email/Google).
- Free tier: 1 free check.
- Paid tier (one-time per-hackathon-cycle pass, or small subscription): unlimited checks, rewrite suggestions, re-check diffing, PDF export.
- Payments via Razorpay (UPI-first, Indian student audience).

## 7. Success metrics
- Activation: % of signups who complete at least one upload → score.
- Conversion: free → paid %.
- Retention within a cycle: % of users who re-check after editing.
- Trust proxy: % of users who share/export their report.
- (Longer-term, if partnerships happen) correlation between predicted score and actual shortlist outcome — this is the real proof the product works.

## 8. Risks
- **Rubric drift risk**: SIH changes format yearly; if the scraper/RAG pipeline lags, the tool scores against a stale rubric and loses trust instantly. Mitigation: human-in-the-loop rubric review, version stamping on every report (see `tech-architecture.md`).
- **Legal/perception risk**: must not imply official affiliation with SIH/AICTE/MoE. Clear disclaimer required on every page and report.
- **LLM cost risk**: technical-depth scoring uses a paid LLM call per submission — must be capped/cached and isolated so a failure doesn't block the rest of the report.
- **Trust risk**: a single opaque number without reasoning will be dismissed as "just another AI toy" — explainability is a core requirement, not a nice-to-have.
- **Data/privacy risk**: decks contain team names, colleges, sometimes personal contact info, and genuinely competitive unpublished ideas. Needs explicit consent language and PII handling (see `tech-architecture.md`).

## 9. Phasing
See `mvp-scope.md` for the detailed MVP vs. V2 vs. V3 feature cut line.

## 10. Legal disclaimer requirement (must ship in MVP)
Every report and the homepage must state, verbatim or equivalent: *"This is an independent tool and is not affiliated with, endorsed by, or officially connected to Smart India Hackathon, AICTE, or the Ministry of Education. Scores are estimates based on publicly available format guidelines and should not be treated as a guarantee of official evaluation outcomes."*
