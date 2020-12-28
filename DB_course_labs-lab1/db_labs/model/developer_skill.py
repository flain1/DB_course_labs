from sqlalchemy import ForeignKey, Integer, Index

from db_labs.db import db


class DeveloperSkill(db.Model):

    developer_id = db.Column(
        Integer, ForeignKey("developer.id", on_delete="CASCADE"), nullable=False
    )
    skill_id = db.Column(
        Integer, ForeignKey("skill.id", on_delete="CASCADE"), nullable=False
    )

    idx_unique_developer_skill = Index(
        "unique_developer_id_skill_id_idx",
        developer_id,
        skill_id,
        unique=True,
    )
