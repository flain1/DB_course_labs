from jetkit.api import CursorPage, searchable_by
from flask_smorest import Blueprint
from db_labs.api.vacancy.schema import VacancySchema
from db_labs.db import BaseQuery
from db_labs.model import Vacancy

blp = Blueprint("Vacancy", __name__, url_prefix=f"/api/vacancy")


@blp.route("", methods=["GET"])
@blp.response(VacancySchema(many=True))
@blp.paginate(CursorPage)  # - it's slow here
@searchable_by(Vacancy.title, search_parameter_name="title")
def get_developers() -> BaseQuery:
    """ Get a paginated list of queries. """

    return Vacancy.query
