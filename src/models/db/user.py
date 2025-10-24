from tortoise.models import Model
from tortoise import fields


class UserDB(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(unique=True, max_length=30)
    avatar_url = fields.CharField(
        max_length=255,
        default="https://i.pinimg.com/736x/03/eb/d6/03ebd625cc0b9d636256ecc44c0ea324.jpg",
    )
    created_at = fields.DatetimeField(auto_now_add=True)
