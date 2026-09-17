-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    college TEXT,
    auth_provider TEXT NOT NULL DEFAULT 'email',
    plan TEXT NOT NULL DEFAULT 'free', -- 'free' or 'paid'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. problem_statements table
CREATE TABLE IF NOT EXISTS problem_statements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    year INT NOT NULL DEFAULT 2026,
    ps_id TEXT NOT NULL, -- e.g. SIH26129
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    theme TEXT,
    category TEXT, -- 'software' or 'hardware'
    embedding VECTOR(384), -- sentence-transformers all-MiniLM-L6-v2 dimension
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast vector similarity search on problem statements
CREATE INDEX IF NOT EXISTS problem_statements_embedding_idx 
ON problem_statements 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 3. rubric_configs table (Rubric-as-Data)
CREATE TABLE IF NOT EXISTS rubric_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    year INT NOT NULL DEFAULT 2026,
    effective_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status TEXT NOT NULL DEFAULT 'active', -- 'draft', 'active', 'archived'
    max_slides INT NOT NULL DEFAULT 6,
    allowed_file_types TEXT[] DEFAULT ARRAY['pdf', 'pptx', 'ppt'],
    max_file_size_mb INT NOT NULL DEFAULT 25,
    required_sections JSONB NOT NULL DEFAULT '[
        {"name": "Title Slide", "keywords": ["title", "team", "ps id", "problem statement id"]},
        {"name": "Problem Statement", "keywords": ["problem", "background", "challenge", "need"]},
        {"name": "Proposed Solution", "keywords": ["solution", "approach", "idea", "innovation"]},
        {"name": "Technical Approach", "keywords": ["tech stack", "architecture", "technology", "feasibility", "implementation"]},
        {"name": "Impact & Benefits", "keywords": ["impact", "benefits", "scalability", "outcomes"]},
        {"name": "References & Team", "keywords": ["references", "team", "members", "contact"]}
    ]'::jsonb,
    category_weights JSONB NOT NULL DEFAULT '{
        "structure_format": 0.15,
        "ps_alignment": 0.20,
        "technical_depth": 0.30,
        "originality": 0.20,
        "clarity": 0.15
    }'::jsonb,
    source_doc_url TEXT,
    source_doc_text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert baseline rubric for SIH 2026
INSERT INTO rubric_configs (
    year, status, max_slides, allowed_file_types, max_file_size_mb, source_doc_text
) VALUES (
    2026, 'active', 6, ARRAY['pdf', 'pptx'], 25,
    'Official SIH 2026 Idea Presentation Format: Maximum 6 slides. Accepted formats: PDF (preferred) and PPTX (up to 25MB). Must cover Title, Problem Statement, Solution, Technical Approach/Tech Stack, Impact & Benefits, and References/Team Details. Paragraphs should be avoided in favor of points, diagrams, and flowcharts.'
) ON CONFLICT DO NOTHING;

-- 4. submissions table
CREATE TABLE IF NOT EXISTS submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    ps_id UUID REFERENCES problem_statements(id) ON DELETE SET NULL,
    rubric_config_id UUID REFERENCES rubric_configs(id),
    file_url TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_type TEXT NOT NULL, -- 'pdf' or 'pptx'
    status TEXT NOT NULL DEFAULT 'queued', -- 'queued', 'processing', 'completed', 'failed'
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. submission_content table
CREATE TABLE IF NOT EXISTS submission_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID REFERENCES submissions(id) ON DELETE CASCADE,
    slide_number INT NOT NULL,
    raw_text TEXT NOT NULL,
    word_count INT DEFAULT 0,
    bullet_count INT DEFAULT 0,
    image_count INT DEFAULT 0,
    embedding VECTOR(384),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. scores table
CREATE TABLE IF NOT EXISTS scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID REFERENCES submissions(id) ON DELETE CASCADE,
    category TEXT NOT NULL, -- 'structure_format', 'ps_alignment', 'technical_depth', 'originality', 'clarity'
    raw_score NUMERIC NOT NULL, -- 0 to 100
    weight_applied NUMERIC NOT NULL, -- e.g. 0.25
    reasons JSONB NOT NULL DEFAULT '[]'::jsonb, -- array of {message, cited_source, slide_number, deduction}
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. reports table
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID UNIQUE REFERENCES submissions(id) ON DELETE CASCADE,
    overall_score NUMERIC NOT NULL, -- 0 to 100
    verdict_text TEXT NOT NULL, -- e.g. 'Strong presentation, meets SIH 2026 guidelines'
    category_breakdown JSONB NOT NULL,
    rewrite_suggestions JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. corpus_documents table (past hackathon decks for originality checking)
CREATE TABLE IF NOT EXISTS corpus_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT NOT NULL,
    year INT DEFAULT 2025,
    title TEXT,
    text_snapshot TEXT NOT NULL,
    embedding VECTOR(384),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for vector search on corpus documents
CREATE INDEX IF NOT EXISTS corpus_documents_embedding_idx 
ON corpus_documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 9. Seed Problem Statements (SIH 2026 Sample Bank)
INSERT INTO problem_statements (ps_id, title, description, theme, category) VALUES
('SIH26101', 'AI-Based Smart Traffic Management System for Urban Cities', 'Develop an intelligent real-time traffic signal optimization system using computer vision and IoT sensors to reduce congestion at urban intersections and prioritize emergency vehicles.', 'Smart Cities', 'software'),
('SIH26102', 'Automated Resume and Presentation ATS Evaluator for Educational Institutions', 'Build an AI tool that evaluates student technical presentations and resumes against standard rubrics, providing line-by-line feedback and actionable improvement recommendations.', 'EdTech', 'software'),
('SIH26103', 'Blockchain-Based Supply Chain Transparency for Agriculture Products', 'Design a decentralized ledger system enabling farmers to track produce from harvest to consumer, ensuring fair pricing and authentic organic certification.', 'AgriTech', 'software'),
('SIH26104', 'IoT-Enabled Water Leakage and Quality Monitoring Network', 'Create a low-cost IoT sensor network for municipal water supply lines that detects chemical contaminants and flow leakages in real-time.', 'Clean & Green Tech', 'hardware'),
('SIH26105', 'Early Detection of Crop Diseases Using Satellite and Drone Imagery', 'Develop a computer vision platform that analyzes drone and multispectral satellite imagery to detect early crop pest infestations and nutrient deficiencies.', 'AgriTech', 'software')
ON CONFLICT DO NOTHING;
