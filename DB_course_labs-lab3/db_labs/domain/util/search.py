from functools import wraps
from typing import Iterable, Tuple

from flask import request
from jetkit.api import append_docs
from sqlalchemy import Column


def combined_search_by(
    *columns: Column,
    search_parameter_name: str = "search",
    joins: Iterable[Tuple[Column, ...]] = (),
):
    def decorator(request_handler):
        @wraps(request_handler)
        def wrapper(*args, **kwargs):
            query = request_handler(*args, **kwargs)
            search_query = request.args.get(search_parameter_name)
            if search_query is None:
                return query

            for join in joins:
                query = query.outerjoin(*join)

            return query.search(search_query, *columns)

        column_names = ", ".join(f"`{column}`" for column in columns)
        append_docs(wrapper, f"`?{search_parameter_name}=` searches by {column_names}")

        return wrapper

    return decorator