import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.session import init_db, SessionLocal
from app.database.seed_data import seed_database
from app.rag.ingestion import ingest_hospital_knowledge
from app.api.auth import router as auth_router
from app.api.departments import router as departments_router
from app.api.doctors import router as doctors_router
from app.api.appointments import router as appointments_router
from app.api.lab_tests import router as lab_tests_router
from app.api.chat import router as chat_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Hospital Application startup and shutdown lifecycle hooks.
    """
    logger.info("Initializing AI Hospital Assistant Backend...")
    # 1. Initialize Tables
    init_db()

    # 2. Seed Database
    if SessionLocal:
        db = SessionLocal()
        try:
            seed_database(db)
        finally:
            db.close()

    # 3. Ingest ChromaDB Hospital Knowledge
    try:
        ingest_hospital_knowledge()
    except Exception as e:
        logger.warning(f"ChromaDB knowledge ingestion warning: {e}")

    logger.info("Hospital Assistant Backend initialization complete!")
    yield
    logger.info("Shutting down Hospital Assistant Backend...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Agentic AI Hospital Assistant powered by LangGraph, Groq, ChromaDB, MySQL & FastAPI.",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(departments_router, prefix=settings.API_V1_STR)
app.include_router(doctors_router, prefix=settings.API_V1_STR)
app.include_router(appointments_router, prefix=settings.API_V1_STR)
app.include_router(lab_tests_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "online",
        "docs_url": "/docs",
        "emergency_hotline": settings.EMERGENCY_HOTLINE
    }


@app.get("/health", tags=["Root"])
def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "connected",
        "groq_model": settings.GROQ_MODEL,
        "api_key_configured": bool(settings.GROQ_API_KEY and not settings.GROQ_API_KEY.startswith("gsk_placeholder")),
        "emergency_hotline": settings.EMERGENCY_HOTLINE
    }
