from jetkit.db.model import TSTZ
from sqlalchemy import Integer, ForeignKey, Text, Index
from db_labs.db import db
from db_labs.model.trgm_extension import TrgmExtension


class Developer(db.Model, TrgmExtension):
    first_name = db.Column(Text)
    last_name = db.Column(Text)
    email = db.Column(Text)
    birthdate = db.Column(TSTZ)

    vacancy_id = db.Column(Integer, ForeignKey("vacancy.id", ondelete="SET NULL"))
    vacancy = db.relationship("Vacancy", back_populates="developers")

    skills = db.relationship("Skill", secondary="developer_skill")

    developer_first_name_trgm_idx = Index('developer_first_name_trgm_idx',
          first_name, postgresql_using='gin',
          postgresql_ops={
              'first_name': 'gin_trgm_ops',
          })

    developer_last_name_trgm_idx = Index('developer_last_name_trgm_idx',
          last_name, postgresql_using='gin',
          postgresql_ops={
              'last_name': 'gin_trgm_ops',
          })


Developer.add_create_trgm_extension_trigger()
