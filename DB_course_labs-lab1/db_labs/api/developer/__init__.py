from typing import Dict, Union

from flask import request
from jetkit.api import combined_search_by
from flask_smorest import Blueprint, abort
from sqlalchemy.orm import joinedload

from db_labs.api.developer.decorators import searchable_by_skills
from db_labs.api.developer.schema import DeveloperSchema
from db_labs.db import db
from db_labs.domain.developer import (
    handle_getting_and_searching_for_developers,
    handle_creating_developer, handle_updating_developer,
)
from db_labs.model import Developer, DeveloperSkill, Skill

blp = Blueprint("Developer", __name__, url_prefix=f"/api/developer")


@blp.route("", methods=["GET"])
@blp.response(DeveloperSchema(many=True))
# @combined_search_by(  # For use with ORM
#     Developer.first_name,
#     Developer.last_name,
#     Skill.name,
#     search_parameter_name="query",
# )
def get_developers():
    """Get all developers(limit is 50 per query) or search for specific developers by first_name,last_name or skill_name."""
    query_string = request.args.get("query")

    developers = handle_getting_and_searching_for_developers(query_string)

    return developers


@blp.route("", methods=["POST"])
@blp.response(DeveloperSchema)
@blp.arguments(DeveloperSchema)
def create_developer(args: Dict[str, str]):
    """Create a developer entry."""
    developer = handle_creating_developer(args)

    return developer


@blp.route("/<string:developer_id>", methods=["PATCH"])
@blp.response(DeveloperSchema)
@blp.arguments(DeveloperSchema)
def update_developer(args: Dict[str, Union[str, int]], developer_id: int):
    """Check if developer with given id exists, then update the entry."""
    developer = handle_updating_developer(args, developer_id)

    return developer
