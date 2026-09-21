import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Uses the container networking defaults from docker-compose.yml
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://aegis:aegis_secure_pass@localhost:5432/aegis"
)

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    """Dependency injection for FastAPI routes."""
    async with AsyncSessionLocal() as session:
        yield session
