from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from models.db import NotificationDB, UserDB
from models.api import NotificationIn, NotificationOut
from dependencies import get_user
from validators import validate_id

router = APIRouter(prefix="/notification")


@router.post("/notifications")
async def create_notification(
    notification: NotificationIn, user: Annotated[UserDB, Depends(get_user)]
):
    db_notification = NotificationDB(
        user_id=user.id, type=notification.type, text=notification.text
    )

    try:
        await db_notification.save()
        return {"detail": "Notification was created"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@router.get("/notifications")
async def get_notifications(
    user: Annotated[UserDB, Depends(get_user)],
) -> list[NotificationOut]:
    raw_notifications = await NotificationDB.filter(user_id=user.id).values()

    notifications = []
    for raw_notification in raw_notifications:
        notifications.append(
            NotificationOut(
                id=raw_notification["id"],
                type=raw_notification["type"],
                text=raw_notification["text"],
                created_at=raw_notification["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
                username=user.username,
                avatar_url=user.avatar_url,
            )
        )

    return notifications


@router.delete("/notifications/{id}")
async def delete_notification(
    id: Annotated[int, Depends(validate_id)],
    user: Annotated[UserDB, Depends(get_user)],
):
    db_notification = await NotificationDB.filter(id=id, user_id=user.id).get_or_none()
    if db_notification:
        await db_notification.delete()
        return {"detail": "Notification was deleted"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Notification does not exists"
    )
