import asyncio

import pytest
from httpx import AsyncClient

from src.core.config import settings

SECRET_KEY = "<KEY>"


@pytest.mark.asyncio
async def test_create_secret(ac: AsyncClient) -> None:
    response = await ac.post(
        "/api/v1/generate",
        json={
            "text": "my text",
            "secret_passphrase": "secret_passphrase",
        },
    )
    assert response.status_code == 201
    data = response.json()
    global SECRET_KEY
    SECRET_KEY = data["secret_key"]


@pytest.mark.asyncio
async def test_get_secret(ac: AsyncClient) -> None:
    response = await ac.post(
        f"/api/v1/secrets/{SECRET_KEY}",
        json={
            "secret_passphrase": "secret_passphrase",
        },
    )
    data = response.json()
    assert data["text"] == "my text"
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_secret(ac: AsyncClient) -> None:
    response = await ac.post(
        f"/api/v1/secrets/{SECRET_KEY}",
        json={
            "secret_passphrase": "secret_passphrase",
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_secret_not_found(ac: AsyncClient) -> None:
    response = await ac.post(
        f"/api/v1/secrets/wrong_secret",
        json={
            "secret_passphrase": "secret_passphrase",
        },
    )
    data = response.json()
    assert data["detail"] == "Secret not found"
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_secret_passphrase_invalid(ac: AsyncClient) -> None:
    add_secret = await ac.post(
        "/api/v1/generate",
        json={
            "text": "my text",
            "secret_passphrase": "secret_passphrase",
        },
    )
    data = add_secret.json()
    secret_key = data["secret_key"]
    response = await ac.post(
        f"/api/v1/secrets/{secret_key}",
        json={
            "secret_passphrase": "WRONG_PASSPHRASE",
        },
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Invalid secret passphrase"


@pytest.mark.asyncio
async def test_secret_expire(ac: AsyncClient) -> None:
    settings.secret_token.expire_time = 1
    add_secret = await ac.post(
        "/api/v1/generate",
        json={
            "text": "my text",
            "secret_passphrase": "secret_passphrase",
        },
    )
    await asyncio.sleep(2)
    data = add_secret.json()
    secret_key = data["secret_key"]
    response = await ac.post(
        f"/api/v1/secrets/{secret_key}",
        json={
            "secret_passphrase": "secret_passphrase",
        },
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Secret expired"
