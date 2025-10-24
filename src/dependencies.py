import os
import jwt

from datetime import datetime
from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models.db import UserDB, TokenDB

security = HTTPBearer()


async def get_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    try:
        decoded_token = jwt.decode(
            credentials.credentials,
            os.environ.get("SECRET_KEY"),
            os.environ.get("ALGORITHM"),
        )

        user_id = decoded_token.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not found user id"
            )

        user = await UserDB.filter(id=decoded_token.get("user_id")).get_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not found user"
            )

        tokens = await TokenDB.filter(user_id=user.id).get_or_none()
        if not tokens:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not found tokens for user",
            )

        # Checking token expire date
        if tokens.access == decoded_token:
            if decoded_token.get("expired") < datetime.now().timestamp():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="access token was expired",
                )
        else:
            if decoded_token.get("expired") < datetime.now().timestamp():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="refresh token was expired",
                )

        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "exception": str(e),
                "creds": credentials.credentials,
                "expr": credentials.credentials != "",
            },
        )
