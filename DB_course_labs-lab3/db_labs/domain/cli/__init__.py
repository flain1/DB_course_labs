from os import abort

import requests

APP_DEV_URL = "http://localhost:5000/api"


def handle_creating_developer(email: str, first_name: str):
    try:
        import requests

        response = requests.post(
            f"{APP_DEV_URL}/developer", json=dict(email=email, first_name=first_name)
        )
    except Exception:
        print("An error occurred while trying to reach the API.")
        return abort()

    if response.status_code != 200:
        print("An error occurred during the API request.")
        return abort()

    return response


def handle_updating_developer(id: int, email: str, first_name: str):
    try:
        response = requests.patch(
            f"{APP_DEV_URL}/developer/{id}",
            json=dict(email=email, first_name=first_name),
        )
    except Exception:
        print("An error occurred while trying to reach the API.")
        return abort()

    if response.status_code != 200:
        print("An error occurred during the API request.")
        return abort()

    return response


def handle_searching_for_developers(query_string: str):
    try:
        response = requests.get(f"{APP_DEV_URL}/developer?query={query_string}")
    except Exception:
        print("An error occurred while trying to reach the API.")
        return abort()

    if response.status_code != 200:
        print("An error occurred during the API request.")
        return abort()

    if not response.json():
        print(f"No results found for the keyword: {query_string}")
        return abort()

    return response


def handle_getting_developers():
    try:
        response = requests.get(f"{APP_DEV_URL}/developer")
    except Exception:
        print("An error occurred while trying to reach the API.")
        return abort()

    if response.status_code != 200:
        print("An error occurred during the API request.")
        return abort()

    if not response.json():
        print(f"No results found")
        return abort()

    return response
