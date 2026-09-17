# Data Schema — SIH-ATS

> Postgres (Supabase/Neon) with the `pgvector` extension enabled. This is a starting schema for vibe-coding the MVP — expect to evolve it, but the shape below already encodes the key architectural decisions (rubric-as-data, feedback loop, PII isolation).

## users
| column | type | notes |
|---|---|---|
| id | uuid, pk | |
| email | text, unique | |
| name | text | |
| college | text, nullable | |
| auth_provider | text | email / google |
| plan | text | free / paid |
| created_at | timestamptz | |

## problem_statements (PS bank, scraped/hosted per cycle)
| column | type | notes |
|---|---|---|
| id | uuid, pk | |
| year | int | e.g. 2026 |
| ps_id | text | official PS code, e.g. SIH26129 |
| title | text | |
| description | text | full official PS text |
| theme | text | |
| category | text | software/hardware |
| embedding | vector | cached embedding of `description`, computed once |

## rubric_configs (the core "rubric-as-data" table — see tech-architecture.md)
| column | type | notes |
|---|---|---|
| id | uuid, pk | |
| year | int | |
| effective_date | date | |
| status | text | draft / active / archived |
| max_slides | int | |
| allowed_file_types | text[] | e.g. {pdf, pptx, ppt} |
| max_file_size_mb | int | |
| required_sections | jsonb | ordered list of {name, keywords, slide_position_hint} |
| category_weights | jsonb | {structure_format, ps_alignment, technical_depth, originality, clarity} |
| source_doc_url | text | |
| source_doc_text | text | full extracted text of the official doc, also embedded into pgvector for citation retrieval |
| created_by | uuid | admin who approved this version |
| created_at | timestamptz | |

## submissions
| column | type | notes |
|---|---|---|
| id | uuid, pk | |
| user_id | uuid, fk → users | |
| ps_id | uuid, fk → problem_statements, nullable | nullable if manually pasted |
| rubric_config_id | uuid, fk → rubric_configs | the version this was scored against — never changes retroactively |
| file_url | text | pointer into S3/R2 |
| file_type | text | |
| status | text | queued / processing / done / failed |
| created_at | timestamptz | |

## submission_content (extracted, parsed data — separated from raw file for reuse without re-parsing)
| column | type | notes |
|---|---|---|
| id | uuid, pk | |
| submission_id | uuid, fk → submissions | |
| slide_number | int | |
| raw_text | text | PII-stripped before any downstream use — see note below |
| font_sizes | jsonb | |
| bullet_count | int | |
| image_count | int | |
| color_palette | jsonb | |
| embedding | vector | per-slide embedding |

## scores
| column | type | notes |
|---|---|---|
| id | uuid, pk | |
| submission_id | uuid, fk → submissions | |
| category | text | structure_format / ps_alignment / technical_depth / originality / clarity |
| raw_score | numeric | |
| weight_applied | numeric | copied from the rubric_config at time of scoring, not looked up live later |
| reasons | jsonb | array of {message, cited_source (nullable), slide_number (nullable)} |
| created_at | timestamptz | |

## reports (aggregated view, one per submission, denormalized for fast frontend reads)
| column | type | notes |
|---|---|---|
| id | uuid, pk | |
| submission_id | uuid, fk → submissions, unique | |
| overall_score | numeric | |
| verdict_text | text | short human-readable summary |
| category_breakdown | jsonb | denormalized copy of `scores` for this submission |
| rewrite_suggestions | jsonb | paid-tier content, nullable for free tier |
| created_at | timestamptz | |

## corpus_documents (past-year decks used for originality scoring)
| column | type | notes |
|---|---|---|
| id | uuid, pk | |
| source | text | e.g. github, slideshare — track provenance/licensing |
| year | int | |
| embedding | vector | full-document embedding |
| text_snapshot | text | PII-stripped |

## feedback_events (the realistic "self-learning" input — see tech-architecture.md)
| column | type | notes |
|---|---|---|
| id | uuid, pk | |
| submission_id | uuid, fk → submissions | |
| predicted_score | numeric | copy of `reports.overall_score` at the time |
| predicted_breakdown | jsonb | |
| actual_outcome | text | shortlisted / not_shortlisted / jury_score / unknown |
| outcome_source | text | self_reported / verified_partner |
| created_at | timestamptz | |

## payments
| column | type | notes |
|---|---|---|
| id | uuid, pk | |
| user_id | uuid, fk → users | |
| razorpay_order_id | text | |
| amount | numeric | |
| status | text | |
| created_at | timestamptz | |

## PII handling note (applies across `submission_content`, `corpus_documents`, `feedback_events`)
A regex/NER pass strips names, phone numbers, emails, and college identifiers from any text field that will be embedded, stored beyond the immediate scoring pass, or used in the corpus/calibration pipeline. Raw uploaded files in object storage are subject to a retention policy (auto-delete after a defined window) — the DB tables above are designed to hold the *derived, PII-stripped* data long-term, not the raw file.
