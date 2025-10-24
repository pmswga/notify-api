from tortoise.models import Model
from tortoise import fields


class TokenDB(Model):
    user_id = fields.IntField(unique=True)
    access = fields.CharField(max_length=2048)
    refresh = fields.CharField(max_length=2048)
