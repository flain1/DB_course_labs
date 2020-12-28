from sqlalchemy import Text

from db_labs.db import db


class Vacancy(db.Model):

    title = db.Column(Text, unique=True, nullable=False)

    developers = db.relationship("Developer", back_populates="vacancy")
