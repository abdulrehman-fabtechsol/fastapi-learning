from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://abdulrehman:aszx1234@postgres_db:5432/fastapi"

# Create an async engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency to get the async database session
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
