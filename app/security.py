# app/security.py
import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("API_KEY", "SECRET_API_KEY_123")
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
