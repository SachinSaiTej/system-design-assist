"""FastAPI application entry point for System Design Assistant."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.design import router as design_router
from api.refine import router as refine_router
from api.section import router as section_router
from api.retrieve_refs import router as retrieve_refs_router
from api.adapt import router as adapt_router

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('system_design_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="System Design Assistant API",
    description="AI-powered system design generation API",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(design_router)
app.include_router(refine_router)
app.include_router(section_router)
app.include_router(retrieve_refs_router)
app.include_router(adapt_router)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.info("🏥 Health check requested")
    return {
        "status": "healthy",
        "message": "System Design Assistant API is running!"
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "System Design Assistant API",
        "version": "1.0.0",
        "docs": "/docs"
    }

logger.info("✅ FastAPI application initialized successfully!")
