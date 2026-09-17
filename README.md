# SIH ATS Scanner — Smart India Hackathon Idea Presentation Evaluator

An "ATS-style" scanner for Smart India Hackathon (SIH) idea presentations — teams upload their PPT/PDF, get an instant, evidence-backed score against the official SIH 2026 rubric, slide-by-slide flags, and line-by-line rewrite suggestions before submitting to the official portal.

---

## Features
- **Official Rubric Compliance**: Evaluates deck against SIH 2026 constraints (Max 6 slides, PDF/PPTX format, required 6-slide structure sequence).
- **Rule-Based Format & Clarity Engine**: Instant zero-cost checks for text density, bullet point ratio, wall-of-text penalties, and visual diagram presence.
- **Problem Statement Alignment**: Cosine similarity using `sentence-transformers` (`all-MiniLM-L6-v2`) and Supabase `pgvector` embeddings against official SIH Problem Statement Bank.
- **Technical Depth AI Judgment**: Gemini 1.5 Flash evaluation for named technology stacks (*FastAPI, PostgreSQL, PyTorch*) vs vague buzzwords (*"Cloud, AI, Database"*).
- **Explainable Deductions & Doc Citations**: Every point lost cites the official SIH 2026 guidelines.
- **Modern UI**: Dark-mode glassmorphism dashboard built with Next.js 14, Tailwind CSS, and Lucide icons.

---

## Architecture & Project Structure

```
sih-ats-scanner/
├── backend/                  # FastAPI (Python 3.11+) Backend
│   ├── app/
│   │   ├── main.py           # FastAPI entry point & CORS configuration
│   │   ├── config.py         # Settings & environment configuration
│   │   ├── database.py       # In-memory & Supabase DB manager
│   │   ├── parsers/          # PPTX & PDF parsing engines
│   │   │   ├── pptx_parser.py
│   │   │   └── pdf_parser.py
│   │   ├── scoring/          # 5 Scoring Category Modules
│   │   │   ├── structure.py  # Slide count & required section sequence
│   │   │   ├── clarity.py    # Text density & visual diagram checks
│   │   │   ├── ps_alignment.py # Sentence embeddings similarity
│   │   │   ├── tech_depth.py # Gemini 1.5 Flash structured tech audit
│   │   │   ├── originality.py# Overlap & template boilerplate check
│   │   │   └── aggregator.py # Weighted score calculation & citations
│   │   └── routers/          # API Endpoints
│   │       ├── submissions.py
│   │       └── problem_statements.py
│   ├── tests/
│   │   └── test_scoring.py   # Test suite for scoring pipeline
│   └── requirements.txt
├── frontend/                 # Next.js 14 App Router Frontend
│   ├── app/
│   │   ├── components/       # Header, UploadSection, ProgressTracker, ReportDashboard
│   │   ├── page.tsx          # Main scan workspace page
│   │   ├── layout.tsx        # Root layout & disclaimers
│   │   └── globals.css       # Glassmorphism & dark theme styles
│   └── package.json
├── database/
│   └── schema.sql            # Supabase PostgreSQL + pgvector schema
└── files/                    # Product specs & rubric baseline docs
```

---

## Getting Started

### 1. Backend Setup (FastAPI)
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

#### Run FastAPI Server:
```bash
uvicorn app.main:app --reload --port 8000
```
API Documentation will be live at: `http://localhost:8000/docs`

#### Environment Variables (Optional):
Create `backend/.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sih_ats
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Note: If `GEMINI_API_KEY` is omitted, the scoring engine uses intelligent rule-based fallback evaluations).*

---

### 2. Frontend Setup (Next.js)
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

### 3. Database Migration (Optional - Supabase / Postgres)
Execute the SQL script in `database/schema.sql` on your Postgres database with `pgvector` enabled.

---

## Legal Disclaimer
This is an independent open-source tool and is not affiliated with, endorsed by, or officially connected to Smart India Hackathon (SIH), AICTE, or the Ministry of Education. Scores are estimates based on publicly available format guidelines.
