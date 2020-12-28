from marshmallow import Schema, fields as f, ValidationError


class BaseSchema(Schema):
    id = f.Integer(dump_only=True)
