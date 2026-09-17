# Rubric Spec — SIH-ATS (current baseline: SIH2026)

> This document is the **seed** for the `rubric_configs` table (see `data-schema.md`). It must be treated as versioned data, not permanent fact — SIH's own format changes yearly. Re-verify against the current official source before each cycle.

## 1. Confirmed official constraints (SIH2026 IDEA Presentation Format, sih.gov.in)
- **Max 6 slides** (not 10 — correcting an earlier draft of this rubric).
- **Submission format**: PDF is the official ask at the AICTE/national level. Some institute-level internal portals additionally accept PPT/PPTX up to ~25MB — support both as upload types, but score against the PDF-equivalent constraints.
- **Required content sections** (mapped to a 6-slide structure used by real submitted decks):
  1. Title Slide — Team Name, PS ID, PS Title, Theme, Organization
  2. Problem Statement / Idea Overview
  3. Proposed Solution / Approach — must explicitly cover: detailed explanation, how it addresses the problem, innovation/uniqueness
  4. Technical Approach / Feasibility & Tech Stack — must name specific technologies, not just categories
  5. Impact & Benefits — social/economic/environmental
  6. Research & References / Team Details
- Explicit formatting instruction from the official doc: use **points, diagrams, and infographics — not paragraphs.**

## 2. Category weights (baseline, adapted from an observed institute-level internal jury rubric — treat as a strong starting point, recalibrate via the feedback loop once real outcome data exists)

| Category | Weight | Scoring method |
|---|---|---|
| Problem understanding & innovation | 20% | Embeddings (PS alignment) + LLM judgment on stated uniqueness |
| Technical approach & feasibility | 25% | LLM-assisted (single call, rubric-prompted) |
| Prototype / implementation plan | 25% | LLM-assisted + rule-based check for presence of a roadmap/timeline |
| Impact & scalability | 20% | LLM-assisted, checks for concrete impact claims vs vague statements |
| Presentation clarity | 10% | Pure rule-based |

Note: this shifts significantly from the generic "resume-ATS-style" weighting drafted earlier in this project's exploration (which over-weighted pure formatting). Content quality (technical approach + prototype plan = 50% combined) should dominate — this matches how actual SIH eliminations are described (vague tech talk kills decks far more than a slightly-off font size).

## 3. Detailed scoring logic per category

### 3.1 Structure & Format compliance (gate, not a soft score)
- Slide count ≤ current `rubric_configs.max_slides` (currently 6). Over the limit → heavy penalty + explicit flag, not silent scoring.
- File type matches accepted types for the current cycle.
- File size within current limit.
- All required sections detected (via heading/keyword + structural position matching against the 6-slide template above).
- **This category should behave like a checklist/gate more than a weighted score** — missing a mandatory section is a bigger problem than a suboptimal font size. Consider representing this as pass/fail sub-checks that feed into, but don't fully determine, the numeric score.

### 3.2 Problem Statement alignment
- Embed the official PS text (once, cached) and embed the "Problem Statement" + "Proposed Solution" slide content.
- Cosine similarity threshold bands (e.g. >0.75 strong, 0.5–0.75 moderate, <0.5 flag as potential drift) — thresholds must be tuned empirically once real data exists, not treated as fixed truth from day one.
- Low similarity → explicit warning: "Your solution slide may not clearly address the selected Problem Statement" — this maps to a real, commonly cited disqualifier.

### 3.3 Technical depth (single LLM call, not per-slide)
- Input: the Technical Approach/Feasibility slide's extracted text.
- Prompt asks for: (a) are specific technologies/methods named, (b) is there a "how," not just a "what," (c) a 1–10 score with a one-line reason.
- This is the one place a real judge-style qualitative read is worth the LLM cost — keep it to 1–2 calls per report max.

### 3.4 Originality / overlap
- Embed the full submission, compare against a growing pgvector corpus of publicly available past-year decks (GitHub repos, SlideShare, etc. — respect source licensing/ToS when building this corpus).
- Flag if similarity crosses a threshold — framed to the user as "this section closely resembles publicly available past submissions," not an accusation, since false positives are likely early on.

### 3.5 Presentation clarity (pure rules, zero AI cost)
- Text density per slide (word count as a proxy for "wall of text").
- Bullet count per slide.
- Font size minimum.
- Diagram/image presence vs text-only slide ratio.
- Color palette consistency (distinct fill colors used across the deck).

## 4. Explainability requirement
Every deduction in every category must produce a human-readable reason. Where the deduction stems directly from an official constraint (slide count, file type, missing section), cite the rubric source doc excerpt. Where it stems from a qualitative LLM judgment, show the model's stated one-line reason rather than just a number.

## 5. Versioning rule
- Every `rubric_configs` row has `year`, `effective_date`, and `status`.
- Never mutate an active rubric config in place — create a new version and mark the old one `archived`. This keeps historical reports accurate to what they were actually scored against.
