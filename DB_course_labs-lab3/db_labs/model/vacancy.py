from jetkit.db.utils import on_table_create
from sqlalchemy import Text, DDL

from db_labs.db import db


class Vacancy(db.Model):

    title = db.Column(Text, unique=True, nullable=False)

    developers = db.relationship("Developer", back_populates="vacancy")

# When a vacancy entry is updated, update recruitment_status on all developers related to it to be "in_progress". In case the vacancy is deleted, mark all devs as "rejected"
on_table_create(Vacancy,
    DDL(
       """
       DROP FUNCTION IF EXISTS update_developers_on_vacancy_update_or_delete() CASCADE;
        CREATE FUNCTION update_developers_on_vacancy_update_or_delete() RETURNS trigger AS $$
        BEGIN
            IF NEW.id THEN
                UPDATE developer set recruitment_status = 'in_progress' where vacancy_id = NEW.id;
            ELSE
                UPDATE developer set recruitment_status = 'rejected' where vacancy_id = OLD.id;
                DELETE FROM vacancy where id = OLD.id;
            END IF;
            RETURN NEW;
        END;
          $$ LANGUAGE 'plpgsql';
        CREATE TRIGGER update_latest_vacancy_stage_trigger BEFORE UPDATE OR DELETE ON vacancy
        FOR EACH ROW WHEN (pg_trigger_depth() = 0) EXECUTE PROCEDURE update_developers_on_vacancy_update_or_delete();
       """
    ))
