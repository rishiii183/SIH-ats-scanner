# User Flow — SIH-ATS

## 1. First-time visitor (landing page)
- Headline states the value prop plainly: "Check your SIH idea PPT before you submit it."
- Immediate, low-friction entry point: "Upload & check free" — do not force signup before the first value moment if avoidable (consider allowing 1 anonymous check, then gate the report behind signup to capture the lead).
- Clear disclaimer visible: not officially affiliated with SIH/AICTE/MoE.
- Social proof / example report screenshot to build trust before upload.

## 2. Sign up
- Email or Google auth.
- Minimal required fields at signup: name, college (optional autocomplete list), email.
- No credit card required for free tier.

## 3. Problem statement selection
- Searchable dropdown/autocomplete over the current year's official PS bank (pre-scraped and hosted, not free text) — this is what makes alignment scoring reliable.
- If a team can't find their PS (rare/edge case), allow manual paste as a fallback, flagged internally as lower-confidence for alignment scoring.

## 4. Upload
- Drag-and-drop or file picker for `.pptx` or `.pdf`.
- Immediate client-side validation: file type, size limit (per current rubric config — surfaced dynamically, not hardcoded in the frontend).
- Confirmation screen: PS selected, filename, "Start check" button.

## 5. Processing (this is a common drop-off point — design it deliberately)
- Progress indicator with staged, human-readable steps rather than a spinner: "Parsing slides… Checking structure… Comparing to problem statement… Scoring technical depth… Finalizing report."
- Expected time shown ("usually under 60 seconds").
- If it's taking long (LLM call latency), don't let the whole UI feel stuck — show partial completion if the backend supports incremental status.

## 6. Report page
- Top: big overall score /100, one-line verdict ("Strong shot at shortlisting" / "Needs work before submitting"), rubric version stamp ("Scored against SIH2026 official format, published [date]").
- Category breakdown cards (Structure & Format, PS Alignment, Technical Depth, Originality, Clarity), each color-coded pass/warn/fail with the weight shown.
- Expandable per-slide feedback: click a category to see exactly which slide(s) triggered a deduction and why, with a citation back to the official doc wording where applicable.
- Concrete rewrite suggestions where relevant (paid feature — free tier sees the *what's wrong*, paid tier also sees the *suggested fix*).
- Actions: "Export as PDF," "Copy shareable link," "Re-check after edits" (paid).

## 7. Paywall moment
- Free tier: 1 full check, sees all deductions and reasoning, but rewrite suggestions and re-check diffing are blurred/locked with a clear upgrade CTA.
- Paid tier: one-time pass per SIH cycle (simpler mental model for students than a recurring subscription) or a low-cost monthly plan if you want recurring revenue — validate which converts better.
- Razorpay checkout (UPI-first).

## 8. Re-check / diff flow (paid)
- User edits their deck based on feedback, re-uploads.
- Report shows a delta view: "Score: 64 → 81 (+17)" with which categories improved and which didn't move.
- This is the retention loop — design it to feel like visible progress, not just a repeated scan.

## 9. Team/SPOC flow (later phase, not MVP)
- A college SIH nodal cell signs up as an "institute" account.
- Bulk upload or a shared portal link where multiple teams submit under one institute.
- Dashboard: all teams' scores, sortable, for internal shortlisting before forwarding to the national portal.
- This is the B2B upsell — do not build until the individual-user product has traction, per `mvp-scope.md`.

## 10. Edge cases to design for explicitly
- Empty/scanned PDF (image-only slides) → OCR fallback triggers, user sees a note that OCR was used and results may be less precise.
- PPT exceeds slide count → still scores, but Structure & Format category is capped/heavily penalized with a clear explanation, not a hard rejection (teams should still see their content-quality scores).
- User uploads a completely unrelated file (e.g. a resume) → detect low relevance early (e.g. no PS-related content at all) and short-circuit with a friendly "this doesn't look like an SIH idea deck" message rather than returning a nonsense score.
