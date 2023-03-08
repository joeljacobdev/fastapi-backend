import asyncio
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

Base = declarative_base()

POSTGRES_DSN = "postgresql+asyncpg://joel:joeljacob@0.0.0.0:9500/fastapi-sqlalchemy"
# we allow 210 connections in db - and we run with 2 worker and each worker we have a single app having 80+20 connections
# max conn we will use = 2*(80+20) = 200 (we can at max increase the connections by 5)
engine = create_async_engine(
    POSTGRES_DSN, echo=False, future=True, pool_size=80, max_overflow=20
)
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, future=True
)
""":type: sqlalchemy.orm.AsyncSession"""


async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            raise
        finally:
            # TODO - only do this if there is any write made
            await session.commit()


async def init_database():
    # TODO if anything needs to be created

    async with engine.begin() as conn:
        # TODO - only to be used for local dev, till migrations are setup
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
