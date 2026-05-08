"""
B_TEA Backend - Main FastAPI Application
Intelligent Expense Analysis Platform
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.utils.logger import get_logger
from app.utils.config import settings

# Initialize logger
logger = get_logger(__name__)

# Startup and Shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown events"""
    logger.info("🚀 B_TEA Backend Starting...")
    logger.info(f"Environment: {settings.ENV}")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    yield
    logger.info("🛑 B_TEA Backend Shutting Down...")

# Create FastAPI app
app = FastAPI(
    title="B_TEA API",
    description="Intelligent Expense Analysis Platform",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns: { status: "healthy", environment: str, version: str }
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "environment": settings.ENV,
            "version": "0.1.0",
            "service": "B_TEA Backend"
        }
    )

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Welcome to B_TEA - Intelligent Expense Analysis Platform",
        "docs": "/docs",
        "health": "/health",
        "version": "0.1.0"
    }

# TODO: Import and include routers
# from app.api.routes import analysis, insights, forecast
# app.include_router(analysis.router, prefix="/api/v1")
# app.include_router(insights.router, prefix="/api/v1")
# app.include_router(forecast.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Uvicorn server...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENV == "development",
        log_level="info"
    )
