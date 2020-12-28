from functools import wraps
from typing import Callable
from flask import request
from sqlalchemy.orm import Query
from db_labs.model import Developer, Skill


def searchable_by_skills(search_parameter_name: str, list_separator: str):
    """
    Allows filtering developers by multiple skills at once.


    For example, when used like this...

    `@searchable_by_skills(search_parameter_name="skills", list_separator=",")`

    ...will allow to filter out only those developers, that have all of the provided
    skills.

    `/api/v1/developers?skills=node,python` -- will return developers that have both
    Python and Node among their skills.
    """

    def decorator(request_handler: Callable[..., Query]):
        @wraps(request_handler)
        def decorated_handler(*args, **kwargs) -> Query:
            query = request_handler(*args, **kwargs)
            search_query = request.args.get(search_parameter_name)

            if not search_query:
                return query

            searched_skills = [
                skill.strip() for skill in search_query.split(list_separator)
            ]

            if search_query is not None:
                query = query.filter(
                    *(
                        Developer.skills.any(Skill.name.ilike(f"%{skill}%"))
                        for skill in searched_skills
                    )
                )

            return query

        return decorated_handler

    return decorator
