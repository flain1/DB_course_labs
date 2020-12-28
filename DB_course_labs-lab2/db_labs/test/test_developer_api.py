def test_creating_developer(client):
    developer = dict(
        first_name="Dmytro", last_name="Yankovskyi", email="test@gmail.com"
    )

    response = client.post("/api/developer", json=developer)

    assert response.status_code == 200

    assert response.json["first_name"]
    assert response.json["last_name"]
    assert response.json["email"]
    assert not response.json["birthdate"]


def test_updating_developer(developer_factory, db_session, client):
    developer = developer_factory(
        first_name="Dmytro", last_name="Yankovskyi", email="test@gmail.com"
    )
    db_session.add(developer)
    db_session.commit()

    updated_first_name = "Testerino"

    response = client.patch(
        f"/api/developer/{developer.id}", json=dict(first_name=updated_first_name)
    )

    assert response.status_code == 200

    assert response.json["first_name"] == updated_first_name
    assert response.json["last_name"]
    assert response.json["email"]
    assert response.json["birthdate"]

    non_existant_developer_id = 9000

    response = client.patch(
        f"/api/developer/{non_existant_developer_id}",
        json=dict(first_name=updated_first_name),
    )

    assert response.status_code == 404


def test_combined_search_on_developer(developer_factory, db_session, client):
    developer1 = developer_factory(first_name="Dmytro", last_name="Yankovskyi")
    developer2 = developer_factory(first_name=developer1.last_name, last_name="Dmytro")

    db_session.add_all([developer1, developer2])

    db_session.commit()

    skill1 = developer1.skills[0]

    query_string = developer1.last_name

    # Test getting all entites in the result due to the combined search via `query_string`
    response = client.get(f"/api/developer?query={query_string}")

    assert response.status_code == 200
    assert len(response.json) == 2

    developer2.first_name = query_string[
        ::-1
    ]  # Change last name to a different one so we can see the entry not included into the result
    db_session.commit()

    response = client.get(f"/api/developer?query={query_string}")
    assert response.status_code == 200
    assert len(response.json) == 1

    query_string = skill1.name

    response = client.get(
        f"/api/developer?query={query_string}"
    )  # Test searching by skill name

    assert response.status_code == 200
    assert len(response.json) == 1
