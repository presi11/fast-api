from tortoise import fields
from tortoise.models import Model


class Dog(Model):
    name = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255)
    picture = fields.CharField(max_length=255)
    is_adopted = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True, description="Created datetime")
