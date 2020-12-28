from sqlalchemy import Text, Index
from db_labs.db import db
from db_labs.model.trgm_extension import TrgmExtension


class Skill(db.Model, TrgmExtension):
    name = db.Column(Text, unique=True, nullable=False)

    developers = db.relationship("Developer", secondary="developer_skill")

    skill_name_trgm_idx = Index('skill_name_trgm_idx',
          name, postgresql_using='gin',
          postgresql_ops={
              'name': 'gin_trgm_ops',
          })


Skill.add_create_trgm_extension_trigger()
