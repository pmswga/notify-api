from tortoise.models import Model
from tortoise import fields

from models.core.notification import NotificationType


class NotificationDB(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.IntField()
    type = fields.IntEnumField(NotificationType)
    text = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
