from db_labs.api.schemas import BaseSchema
from marshmallow import fields as f


class VacancySchema(BaseSchema):
    title = f.Str(required=True)
