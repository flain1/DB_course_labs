from typing import Dict, Union
from jetkit.api import CursorPage
from flask_smorest import Blueprint, abort
from sqlalchemy.orm import joinedload
from db_labs.api.developer.decorators import searchable_by_skills
from db_labs.api.developer.schema import DeveloperSchema
from db_labs.db import db
from db_labs.domain.util.search import combined_search_by
from db_labs.model import Developer, Skill

blp = Blueprint("Developer", __name__, url_prefix=f"/api/developer")


@blp.route("", methods=["GET"])
@blp.response(DeveloperSchema(many=True))
@blp.paginate(CursorPage)
@combined_search_by(
    Developer.first_name, Developer.last_name
)
def get_developers():
    """Get a paginated list of devs or search for specific developers by first_name,last_name or skill_name."""

    return Developer.query


@blp.route("", methods=["POST"])
@blp.response(DeveloperSchema)
@blp.arguments(DeveloperSchema)
def create_developer(args: Dict[str, str]):
    """Create a developer entry."""

    #  All CRUD methods can be generalized and use a generic controller method here. In this small lab it'd be redundant.
    developer = Developer(**args)

    db.session.add(developer)

    db.session.commit()

    return developer


@blp.route("/<int:developer_id>", methods=["PATCH"])
@blp.response(DeveloperSchema)
@blp.arguments(DeveloperSchema)
def update_developer(args: Dict[str, Union[str, int]], developer_id: int):
    """Check if developer with given id exists, then update the entry."""

    #  All CRUD methods can be generalized and use a generic controller method here. In this small lab it'd be redundant.

    # remove None values so they do not override existing data.
    values = {key: value for key, value in args.items() if value is not None}

    developer = Developer.query.filter(Developer.id == developer_id).one_or_none()

    if not developer:
        abort(404, message="Couldn't find developer to update.")

    for attr, value in values.items():
        if hasattr(developer, attr):
            setattr(developer, attr, value)

    db.session.commit()

    return developer


@blp.route("/<int:developer_id>", methods=["DELETE"])
@blp.response()
def delete_developer(developer_id: int):
    """Check if developer with given id exists, then update the entry."""

    #  All CRUD methods can be generalized and use a generic controller method here. In this small lab it'd be redundant.
    developer = Developer.query.filter(Developer.id == developer_id).one_or_none()

    if not developer:
        abort(404, message="Couldn't find developer to update.")

    db.session.delete(developer)

    db.session.commit()
