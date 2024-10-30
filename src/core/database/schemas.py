from pydantic import BaseModel


class GenerateCreate(BaseModel):
    text: str
    secret_passphrase: str


class GenerateOutput(BaseModel):
    secret_key: str


class SecretResponse(BaseModel):
    text: str


class SecretInput(BaseModel):
    secret_passphrase: str
