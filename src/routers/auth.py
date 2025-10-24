import jwt
import os

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from models.db import UserDB, TokenDB
from models.api import UserRegisterIn, UserLogin, UserRegisteredOut
from dependencies import get_user

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(user: UserRegisterIn) -> UserRegisteredOut | dict:
    is_user_exist = await UserDB.filter(username=user.username).get_or_none()
    if is_user_exist:
        return {"msg": "User is already registered", "status": "error"}

    db_user = UserDB(username=user.username)

    try:
        await db_user.save()

        expired = datetime.now() + timedelta(
            minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )
        access_token = jwt.encode(
            {
                "user_id": db_user.id,
                "expired": expired.timestamp(),
            },
            os.environ.get("SECRET_KEY"),
            os.environ.get("ALGORITHM"),
        )
        refresh_token = jwt.encode(
            {"user_id": db_user.id, "used": False},
            os.environ.get("SECRET_KEY"),
            os.environ.get("ALGORITHM"),
        )

        token = await TokenDB.create(
            user_id=db_user.id, access=access_token, refresh=refresh_token
        )

        return UserRegisteredOut(
            user_id=db_user.id, access=token.access, refresh=token.refresh
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/login")
async def login(user: UserLogin):
    db_user = await UserDB.filter(username=user.username).get_or_none()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist"
        )

    token = await TokenDB.filter(user_id=db_user.id).get_or_none()

    if token:
        return {"access": token.access, "refresh": token.refresh}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No tokens for user"
        )


@router.post("/refresh")
async def refresh(
    user: Annotated[UserDB, Depends(get_user)],
):
    return None
