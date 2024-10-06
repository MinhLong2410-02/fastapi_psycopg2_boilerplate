from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import models, os

# Load environment variables or use a configuration module
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize connection pool
engine = create_async_engine(DATABASE_URL, echo=True)

# Async session maker
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create the database tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)