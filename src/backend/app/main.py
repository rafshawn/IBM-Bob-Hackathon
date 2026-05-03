"""
PublicPulse AI - FastAPI Application
Main entry point for the backend API
"""
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db
from app.schemas import HealthCheck
from app.routers import scans, issues, pages, recommendations

# Initialize FastAPI application
app = FastAPI(
    title="PublicPulse AI API",
    description="AI-powered website auditing platform for public service organizations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Startup and Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✅ Database initialized")
    print(f"✅ API running on http://{settings.api_host}:{settings.api_port}")
    print(f"✅ API docs available at http://{settings.api_host}:{settings.api_port}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Shutting down PublicPulse AI API")


# ============================================================================
# Root and Health Check Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "PublicPulse AI API",
        "version": "1.0.0",
        "description": "AI-powered website auditing platform",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthCheck, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow(),
        database="connected",
        features={
            "ai_recommendations": settings.enable_ai_recommendations,
            "auto_fix_preview": settings.enable_auto_fix_preview,
            "batch_processing": settings.enable_batch_processing
        }
    )


# ============================================================================
# Include Routers
# ============================================================================

app.include_router(
    scans.router,
    prefix="/api/v1/scans",
    tags=["Scans"]
)

app.include_router(
    issues.router,
    prefix="/api/v1/issues",
    tags=["Issues"]
)

app.include_router(
    pages.router,
    prefix="/api/v1/pages",
    tags=["Pages"]
)

app.include_router(
    recommendations.router,
    prefix="/api/v1/recommendations",
    tags=["Recommendations"]
)


# ============================================================================
# Global Exception Handlers
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "detail": "The requested resource was not found",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ============================================================================
# Run Application
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )

# Made with Bob
