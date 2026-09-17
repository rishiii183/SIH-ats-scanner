from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import problem_statements, submissions

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(problem_statements.router, prefix=settings.API_V1_STR)
app.include_router(submissions.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "message": "SIH ATS Scanner API is running.",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
