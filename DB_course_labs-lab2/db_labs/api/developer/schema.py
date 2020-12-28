from marshmallow import fields as f

from db_labs.api.schemas import BaseSchema
from db_labs.api.skill.schema import SkillSchema
from db_labs.api.vacancy.schema import VacancySchema


class DeveloperSchema(BaseSchema):
    skills = f.Nested(SkillSchema(many=True))
    first_name = f.Str()
    last_name = f.Str()
    email = (
        f.Str()
    )  # Could be f.Email(), but if we generate random strings with raw SQL, it'd be better to have it f.Str() for simplicity's sake
    birthdate = f.DateTime()
    vacancy = f.Nested(VacancySchema)
