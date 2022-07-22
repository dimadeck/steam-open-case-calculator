import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings_app

dsn = settings_app.dsn

engine = create_async_engine(dsn, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, autocommit=False, class_=AsyncSession)

metadata = sqlalchemy.MetaData()
Base = declarative_base(metadata=metadata)
