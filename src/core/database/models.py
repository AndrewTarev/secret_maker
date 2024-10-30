import asyncio
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import DeclarativeBase

from src.core.database.db_helper import db_helper


class Base(DeclarativeBase):
    pass


class Secret(Base):
    __tablename__ = "secrets"
    code = Column(String, primary_key=True)
    secret_passphrase = Column(String, nullable=False)
    text = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)


async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await db_helper.engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_tables())
