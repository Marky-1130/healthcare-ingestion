from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

# =========================
# SYNC DATABASE
# =========================

sync_engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False,
)

# =========================
# ASYNC DATABASE
# =========================

async_engine = create_async_engine(settings.DATABASE_URL_ASYNC, pool_pre_ping=True)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# =========================
# BASE
# =========================

Base = declarative_base()

# =========================
# SYNC DEPENDENCY
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# ASYNC DEPENDENCY
# =========================

async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db