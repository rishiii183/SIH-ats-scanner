# Tech Architecture — SIH-ATS

## 1. High-level system diagram (textual)

```
[Next.js Frontend] --> [FastAPI API] --> [Postgres (Supabase/Neon) + pgvector]
                              |
                              v
                        [Redis Queue]
                              |
                              v
                     [Celery/RQ Workers] --> [S3 / R2 Storage]
                              |
                              +--> Parsing (python-pptx, PyMuPDF, OCR fallback)
                              +--> Rule-based scoring (Structure & Format, Clarity)
                              +--> Embedding scoring (sentence-transformers + pgvector)
                              +--> LLM call (Claude/GPT — Technical Depth only)
                              |
                              v
                     [Report written to Postgres] --> [Frontend polls/websocket] --> [User]

[Scraper Job (scheduled)] --> [Official SIH doc source] --> [Diff vs stored rubric] --> [Admin review queue] --> [rubric_configs table]
```

## 2. Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | Next.js + Tailwind, deployed on Vercel | Fast to ship, React Query for polling job status |
| API | FastAPI (Python) | Same language as parsing/ML stack, avoids cross-language glue |
| Queue | Redis + Celery (or RQ for simplicity) | PPT parsing + embeddings are CPU/IO heavy — never block the request thread |
| Parsing (pptx) | `python-pptx` | Native text, fonts, shapes, colors — no OCR needed for native files |
| Parsing (pdf) | `PyMuPDF` (+ `pdf2image`), OCR fallback via `pytesseract` or a vision-LLM call only if text extraction is empty (flattened/scanned decks) | Covers both submission formats the official portal accepts |
| Embeddings | `sentence-transformers` (e.g. `all-MiniLM-L6-v2` or a stronger multilingual model), self-hosted | Free/cheap at volume — do not pay per-call to an LLM for every similarity check |
| Vector store | pgvector (extension on the same Postgres) | No need for a separate vector DB until real scale problems appear |
| LLM (sparingly) | Claude or GPT API — 1–2 calls per report max | Reserved for technical-depth judgment and rewrite suggestions; never used for bulk comparisons |
| DB | Postgres (Supabase or Neon) | Supabase also bundles auth |
| Auth | Supabase Auth or Clerk | Managed, fast to integrate |
| Payments | Razorpay | UPI support matters for the Indian student audience |
| Storage | Cloudflare R2 (or S3) | R2 avoids egress fees |

## 3. Processing flow (one submission)

1. User uploads file → goes straight to object storage, DB row created with status `queued`.
2. API enqueues a job (do not process synchronously — parsing + embeddings can take 5–20s).
3. Worker picks up job:
   a. Extract raw text per slide, slide count, fonts/sizes, images, color palette, layout metadata.
   b. Run scoring modules **in parallel where possible**:
      - Structure & Format (pure rules, reads live from current `rubric_configs` row — never hardcoded)
      - Problem Statement Alignment (embed PS text + slide text, cosine similarity via pgvector)
      - Originality (embed submission, compare against corpus of past decks in pgvector)
      - Presentation Clarity (rules: text density, bullet count, diagrams-vs-text ratio, font size)
      - Technical Depth (single LLM call with the technical-approach slide's text + a rubric prompt)
   c. Aggregate into weighted score using the active `rubric_configs` weights.
   d. Write report (score breakdown + reasons, each citing the relevant rubric/doc excerpt where applicable) to DB.
4. Frontend polls (or subscribes via websocket) for job completion, renders report.

**Failure isolation rule**: if the LLM call for technical depth times out or errors, the rest of the report (75%+ of the score) must still render, with that one section marked "pending retry" — never block the whole report on one module.

## 4. Rubric-as-data, not rubric-as-code

The single most important architectural decision: **the scoring rubric lives in the database, versioned, not hardcoded in the scoring logic.**

- `rubric_configs` table: `id, year, effective_date, max_slides, allowed_file_types, max_file_size_mb, required_sections (jsonb), category_weights (jsonb), source_doc_url, source_doc_text, status (draft/active/archived)`.
- Every scored submission stores which `rubric_config_id` was used, so a report always shows *"Scored against SIH2026 official format, effective [date]"* — this is both a trust signal and a debugging necessity when rules change mid-cycle.
- Scoring code reads the active config at runtime. Updating the rubric is a DB write + admin approval, never a redeploy.

## 5. RAG pipeline for rubric freshness

Because SIH changes format almost every year and publishes inconsistently (sometimes PDF, sometimes PPTX, buried in a "Letters" page), full automation is unsafe. Use a **human-in-the-loop RAG pipeline**, not blind auto-apply:

1. Scheduled scraper (cron — monthly off-season, weekly starting ~August when SIH typically announces) checks a small allowlist of trusted sources (official SIH site + any officially linked doc URLs).
2. Diff the fetched doc text against the last stored version.
3. If changed: do **not** auto-apply. Push to an admin review queue with the diff highlighted.
4. On human approval, parse the confirmed doc into a new `rubric_configs` row (new `effective_date`) and embed the doc text into pgvector.
5. The embedded doc text is retrieved at report-generation time so deduction reasons can cite the actual source language ("Official format requires ≤6 slides") instead of a hardcoded string — this is the actual "RAG" in the system: retrieval for *explanation*, not for generating the rubric itself.

## 6. Feedback loop / calibration (the realistic version of "self-learning")

Do **not** attempt online/autonomous retraining. Instead:

- `feedback_events` table: `submission_id, predicted_score, predicted_breakdown (jsonb), actual_outcome (shortlisted/not/jury_score/self_reported), source (self_reported/verified_partner), created_at`.
- Collect self-reported outcomes ("did you get shortlisted?") and, where possible, partner with a few colleges' SIH nodal cells for verified jury scores.
- Run an **offline, scheduled batch job** (weekly) that checks correlation between category scores and actual outcomes, and proposes weight adjustments — reviewed by a human before being applied to a new `rubric_configs` version.
- The **originality/plagiarism module** genuinely improves passively as the pgvector corpus of past decks grows — no retraining needed, just corpus growth.
- A lightweight classifier for "vague vs specific technical language" can be improved via a growing few-shot example set (human-labeled) rather than model fine-tuning at this stage.

## 7. Privacy & compliance

- PII (team member names, phone numbers, emails, sometimes college IDs) must be stripped via a regex/NER pass **before** any file content is embedded, stored long-term, or used for corpus/calibration purposes.
- Explicit opt-in consent (not pre-checked, not buried) required for "we may use anonymized/aggregated submission data to improve scoring" — required under India's DPDP Act 2023 since decks contain personal data.
- Retention policy: auto-delete raw uploaded files after a defined window (e.g. end of that SIH cycle + N months); retain only extracted, PII-stripped features/scores for model calibration.

## 8. Scalability notes (don't over-build early)
- Redis + Celery workers can be horizontally scaled independently of the API as submission volume grows near deadlines (expect huge traffic spikes right before SIH submission dates — this is the actual load pattern to design for, not steady traffic).
- pgvector is sufficient until corpus size or query volume genuinely outgrows Postgres — don't add a dedicated vector DB (Pinecone etc.) preemptively.
- Cache Problem Statement embeddings — thousands of teams share the same ~50–200 official PS, embed each once, not per submission.
