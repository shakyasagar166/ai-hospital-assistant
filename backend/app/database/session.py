import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
from app.database.models import Base

logger = logging.getLogger(__name__)

engine = None
SessionLocal = None


def create_app_engine():
    global engine, SessionLocal
    if engine is not None:
        return engine

    mysql_url = settings.get_database_url()
    try:
        logger.info(f"Connecting to MySQL database at {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}...")
        test_engine = create_engine(
            mysql_url,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=10,
            max_overflow=20,
            connect_args={"connect_timeout": 5}
        )
        with test_engine.connect() as conn:
            pass
        engine = test_engine
        logger.info("Successfully connected to MySQL database!")
    except Exception as e:
        logger.warning(
            f"Could not connect to MySQL ({e}). Falling back to local embedded SQLite database for zero-downtime development."
        )
        sqlite_url = "sqlite:///./hospital_local.db"
        engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
        logger.info("Local SQLite engine initialized.")

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine


get_engine = create_app_engine

# Eagerly initialize engine & SessionLocal on import
create_app_engine()


def init_db():
    global engine
    if engine is None:
        create_app_engine()
    Base.metadata.create_all(bind=engine)
    logger.info("Hospital database tables initialized successfully.")


def get_db():
    global SessionLocal
    if SessionLocal is None:
        create_app_engine()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
