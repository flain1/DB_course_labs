from db_labs.api.schemas import BaseSchema
from marshmallow import fields as f


class SkillSchema(BaseSchema):
    name = f.Str(required=True)
