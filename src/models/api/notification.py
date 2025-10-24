from models.core.notification import NotificationType

from pydantic import BaseModel


class NotificationIn(BaseModel):
    type: NotificationType
    text: str


class NotificationOut(BaseModel):
    id: int
    type: NotificationType
    text: str
    created_at: str
    username: str
    avatar_url: str
