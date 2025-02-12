# app/core/jwt_manager.py
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
import jwt
from jwt import PyJWTError
from fastapi import HTTPException, status

# JWT Manager Class
class JWTManager:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decodes a JWT token and returns the payload.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except PyJWTError as e:
            raise HTTPException(
                status_code=401,
                detail=f"Could not validate credentials: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def validate_token_type(self, payload: Dict[str, Any], expected_type: str) -> None:
        """
        Validates the token type (e.g., 'access' or 'refresh').
        """
        token_type = payload.get("type")
        if token_type != expected_type:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid token type: expected {expected_type}, got {token_type}",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_subject(self, payload: Dict[str, Any]) -> str:
        """
        Retrieves the subject (typically username) from the token payload.
        """
        subject = payload.get("sub")
        if subject is None:
            raise HTTPException(
                status_code=401,
                detail="Token payload missing 'sub' claim",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return subject