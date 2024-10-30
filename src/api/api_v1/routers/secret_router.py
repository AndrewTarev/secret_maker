import os
from datetime import datetime, timedelta
from typing import Dict

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.database.db_helper import db_helper
from src.core.database.models import Secret
from src.core.database.schemas import GenerateCreate, SecretResponse, SecretInput, GenerateOutput
from src.core.utils import hmac_passphrase

router = APIRouter(
    tags=["Secret_text"],
)

private_secret_key = settings.secret_token.secret_key


@router.post("/generate", status_code=status.HTTP_201_CREATED, response_model=GenerateOutput)
async def generate_secret(
        secret: GenerateCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
        ) -> Dict[str, str]:
    """Accepts a secret and a passphrase and gives the secret_key by which this secret can be obtained."""
    hashed_passphrase: str = hmac_passphrase(secret.secret_passphrase, private_secret_key)
    time_expier = datetime.utcnow() + timedelta(seconds=settings.secret_token.expire_time)
    code = os.urandom(32).hex()

    stmt = select(Secret).where(Secret.code == code)
    result = await session.execute(stmt)
    if result.scalars().first() is not None:
        code = os.urandom(32).hex()

    secret_db = Secret(code=code, secret_passphrase=hashed_passphrase, text=secret.text, expires_at=time_expier)
    session.add(secret_db)
    await session.commit()

    return {"secret_key": code}


@router.post("/secrets/{secret_key}", response_model=SecretResponse)
async def get_secret(
        secret_key: str,
        user_input_secret: SecretInput,
        session: AsyncSession = Depends(db_helper.session_getter),
        ) -> Dict[str, str]:
    """Accepts a passphrase as input and gives it to the secretary"""
    stmt = select(Secret).where(Secret.code == secret_key)
    secret_db = await session.execute(stmt)
    result = secret_db.scalars().first()

    if result is None:
        raise HTTPException(status_code=404, detail="Secret not found")

    if hmac_passphrase(user_input_secret.secret_passphrase, private_secret_key) != result.secret_passphrase:
        raise HTTPException(status_code=403, detail="Invalid secret passphrase")

    await session.delete(result)
    await session.commit()

    if result.expires_at < datetime.utcnow():
        raise HTTPException(status_code=404, detail="Secret expired")

    return {"text": result.text}
