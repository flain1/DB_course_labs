from typing import Dict, Union
from flask_smorest import abort
from sqlalchemy.orm import joinedload

from db_labs.db import db
from db_labs.model import Developer, DeveloperSkill, Skill


def handle_getting_and_searching_for_developers(query_string: str):
    """Get all developers(limit is 50 per query) or search for specific developers by first_name,last_name or skill_name."""
    if query_string:
        query_string = f"%{query_string}%"  # Enclosed in '%' as per ILIKE syntax

        # Query for search
        # UNION needed here to speed up ILIKE across 2 tables. SELECT * also fetches vacancy and skills that were JOINed. We don't process and output them however.
        query = """SELECT *
FROM developer LEFT OUTER JOIN developer_skill ON developer.id = developer_skill.developer_id LEFT OUTER JOIN skill ON skill.id = developer_skill.skill_id LEFT OUTER JOIN vacancy AS vacancy_1 ON vacancy_1.id = developer.vacancy_id LEFT OUTER JOIN (developer_skill AS developer_skill_1 JOIN skill AS skill_1 ON skill_1.id = developer_skill_1.skill_id) ON developer.id = developer_skill_1.developer_id
WHERE CAST(developer.first_name AS VARCHAR) ILIKE :query_string ESCAPE '~' OR CAST(developer.last_name AS VARCHAR) ILIKE :query_string ESCAPE '~' UNION SELECT  *
FROM developer LEFT OUTER JOIN developer_skill ON developer.id = developer_skill.developer_id LEFT OUTER JOIN skill ON skill.id = developer_skill.skill_id LEFT OUTER JOIN vacancy AS vacancy_1 ON vacancy_1.id = developer.vacancy_id LEFT OUTER JOIN (developer_skill AS developer_skill_1 JOIN skill AS skill_1 ON skill_1.id = developer_skill_1.skill_id) ON developer.id = developer_skill_1.developer_id
WHERE CAST(skill.name AS VARCHAR) ILIKE :query_string ESCAPE '~' LIMIT 50;"""

        developers = db.session.execute(query, dict(query_string=query_string))
    else:
        query = """SELECT * FROM developer LIMIT 50;"""
        developers = db.session.execute(query)

    return developers


def handle_creating_developer(args: Dict[str, str]):
    # developer = Developer(**args) For ORM
    # db.session.add(developer)
    # db.session.commit()

    create_developer_query = """INSERT INTO developer (first_name, email) VALUES (:first_name, :email) RETURNING developer.id, developer.email, developer.first_name"""

    result = db.session.execute(create_developer_query, args)

    db.session.commit()

    developer = {}
    for entry in result:
        developer = entry

    return developer


def handle_updating_developer(args: Dict[str, Union[str, int]], developer_id: int):
    # developer = Developer.query.get(developer_id)

    # if not developer:
    #     abort(404, message=f"No developer with id: ${developer_id} found.")

    # remove None values so they do not override existing data
    values = {key: value for key, value in args.items() if value is not None}
    # Developer.query.update(values) for ORM

    update_developer_query = """UPDATE developer SET updated_at=NOW(), first_name=:first_name, email=:email WHERE id=:id RETURNING developer.id, developer.email, developer.first_name"""
    values["id"] = developer_id
    result = db.session.execute(update_developer_query, values)

    db.session.commit()

    developer = {}
    for entry in result:
        developer = entry

    if not developer:
        abort(404, message=f"No developer with id: ${developer_id} found.")

    return developer