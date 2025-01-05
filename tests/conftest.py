import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.api.dependencies.session import get_async_session
from main import backend_app
from src.repository.table import Base


@pytest_asyncio.fixture(autouse=True)
@pytest.mark.asyncio
async def override_database():
    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, autoflush=False
    )

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    backend_app.dependency_overrides[get_async_session] = override_get_db

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
