from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator
from .settings import config


engine = create_async_engine(
    url=config.db.url,
    echo=False,
    pool_size=50,
    pool_pre_ping=True,
    max_overflow=0
)


session_fabric = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None, None]:
    async with session_fabric() as session:
        yield session