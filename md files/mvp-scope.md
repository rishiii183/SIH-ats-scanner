# MVP Scope & Phasing — SIH-ATS

## Phase 0 — Before writing product code
- [ ] Manually verify the current cycle's official SIH IDEA Presentation Format doc (don't trust last year's assumptions).
- [ ] Manually populate the first `rubric_configs` row and the `problem_statements` bank for the current year — this can be a one-time manual scrape/paste job, not automated yet.
- [ ] Draft and legally review the non-affiliation disclaimer and the data-consent language (DPDP Act 2023 relevant since decks contain personal data).

## Phase 1 — MVP (ship this first, nothing else)
Goal: prove the core loop — upload → explainable score → someone pays for a second check.

- Auth (email/Google)
- PS bank dropdown (manually seeded, current year only)
- Upload (PPTX + PDF), size/type validation against the active rubric config
- Async processing pipeline: parsing → 5-category scoring → aggregated report
  - Structure & Format: **fully rule-based, ship first, zero AI cost**
  - Presentation Clarity: **fully rule-based, ship first, zero AI cost**
  - PS Alignment: embeddings (needs the PS bank + one embedding model call per submission)
  - Technical Depth: single LLM call, with a hard fallback (report still renders if this fails)
  - Originality: **can be stubbed/deferred to Phase 2** if corpus isn't built yet — do not block MVP launch on having a large corpus; ship the module cheaply with a small seed corpus and get better with time
- Report page: overall score, category breakdown, per-slide reasons, disclaimer
- Free tier: 1 check. Paid tier: unlimited + rewrite suggestions + re-check diff.
- Razorpay payment integration
- Manual admin process for rubric updates (no scraper automation yet — a human checks the official site and updates the DB row directly)

**Explicitly cut from Phase 1**: automated rubric scraper, feedback/calibration pipeline, institute/SPOC bulk dashboard, PDF export, shareable links, any fine-tuned classifier.

## Phase 2 — Retention & trust hardening
- Automated scraper + admin review queue for rubric updates (the RAG pipeline from `tech-architecture.md`)
- Feedback loop: `feedback_events` collection + the offline weekly calibration job
- Grow the originality corpus meaningfully (more sources, licensing-checked)
- PDF export / shareable report links
- Rewrite suggestion quality pass (few-shot prompt refinement using early real submissions)

## Phase 3 — Expansion
- Institute/SPOC bulk-screening dashboard (B2B angle)
- Support for additional file inputs (e.g. Canva export edge cases)
- Possible authoring-assist features (outline generation) — only after scoring product has proven trust; don't blur "checker" positioning too early

## What NOT to build until there's real usage data
- Any autonomous/online-learning model — the feedback loop is a scheduled, human-reviewed batch job, not a live-training system (see `tech-architecture.md`, section 6).
- A dedicated vector DB beyond pgvector.
- A fine-tuned foundation model. Better prompting + a good rubric gets ~90% of the value at a fraction of the cost and risk.
