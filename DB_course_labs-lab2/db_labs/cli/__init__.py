from pprint import pprint
import click
from db_labs.domain.cli import (
    handle_creating_developer,
    handle_updating_developer,
    handle_searching_for_developers,
    handle_getting_developers,
)

APP_DEV_URL = "http://localhost:5000/api"


@click.command()
@click.option(
    "--option",
    prompt="Your name",
    help="Options: create_developer\nupdate_develiper\nsearch_developers",
)
def main(option):
    if option == "create_developer":
        email = click.prompt("Please enter an email", type=str)
        first_name = click.prompt("Please enter a first name", type=str)

        response = handle_creating_developer(email, first_name)

        print("New developer created.")
        return pprint(response.json())

    if option == "update_developer":
        developer_id = click.prompt("Please enter a developer id", type=int)
        email = click.prompt("Please enter an email", type=str)
        first_name = click.prompt("Please enter a first name", type=str)

        response = handle_updating_developer(developer_id, email, first_name)

        print(f"Developer with id: {developer_id} was updated.")
        return pprint(response.json())

    if option == "search_developers":
        query_string = click.prompt(
            "Please enter a search keyword(first/last name or skill name)", type=str
        )

        response = handle_searching_for_developers(query_string)

        print(
            f"{len(response.json())} developers found for the keyword: {query_string}"
        )
        return pprint(response.json())

    if option == "get_developers":
        response = handle_getting_developers()

        print(f"{len(response.json())} developers fetched")
        return pprint(response.json())


if __name__ == "__main__":
    main()
