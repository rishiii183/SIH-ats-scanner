import time
import logging
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.database import DBManager
from app.routers import problem_statements, submissions, payments


# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("sih-ats-backend")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 1. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Performance, Rate Limiting & Security Headers Middleware
@app.middleware("http")
async def production_security_and_logging_middleware(request: Request, call_next):
    # Enforce Rate Limiting
    client_ip = request.client.host if request.client else "127.0.0.1"
    
    # Don't rate limit health checks
    if not request.url.path.endswith("/health"):
        from app.security import rate_limiter
        is_limited, retry_after = rate_limiter.is_rate_limited(client_ip)
        if is_limited:
            logger.warning(f"Rate limit exceeded for IP: {client_ip} on {request.url.path}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "message": f"Rate limit exceeded. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after
                },
                headers={"Retry-After": str(retry_after)}
            )

    start_time = time.time()
    response: Response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    
    # Production Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    logger.info(
        f"HTTP {request.method} {request.url.path} - Status: {response.status_code} - {process_time:.2f}ms"
    )
    return response

# 3. Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred while processing your request.",
            "detail": str(exc) if settings.ENVIRONMENT != "production" else None
        }
    )

# 4. Include API Routers
app.include_router(problem_statements.router, prefix=settings.API_V1_STR)
app.include_router(submissions.router, prefix=settings.API_V1_STR)
app.include_router(payments.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "operational",
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    """
    Production health and readiness probe for load balancers & container orchestrators.
    """
    supabase_connected = DBManager.get_client() is not None
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database_connected": supabase_connected,
        "storage_bucket": settings.SUPABASE_BUCKET,
        "timestamp": time.time()
    }

