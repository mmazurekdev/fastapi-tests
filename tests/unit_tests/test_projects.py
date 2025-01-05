import datetime

import fastapi
import pytest
from fastapi.testclient import TestClient

from main import backend_app


def test_status_code_on_list_projects():
    client = TestClient(backend_app)

    response = client.get("/api/projects")
    assert response.status_code == 200


def test_list_projects():
    # given
    client = TestClient(backend_app)
    _ = client.post(
        "/api/projects",
        json={
            "name": "test",
            "date_range_from": str(datetime.datetime.utcnow()),
            "date_range_to": str(datetime.datetime.utcnow()),
            "geo_file": {
                "type": "test",
                "geometry": {"type": "test", "coordinates": [[[[22.33, 44.55]]]]},
            },
        },
    )

    # when
    response = client.get("/api/projects")

    # then
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "test"


@pytest.mark.parametrize(
    ["invalid_input"],
    [
        [{"name": "test"}],
        [{"description": "desc", "name": "name"}],
        [{"description": "desc", "name": "name", "geo_file": []}],
    ],
)
def test_invalid_input_for_create_project(invalid_input):
    client = TestClient(backend_app)

    response = client.post("/api/projects", json=invalid_input)
    assert response.status_code == fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY


def test_date_range_to_less_than_date_range_from():
    client = TestClient(backend_app)

    response = client.post(
        "/api/projects",
        json={
            "description": "desc",
            "name": "name",
            "coordinates": [],
            "date_range_from": str(
                datetime.datetime.utcnow() + datetime.timedelta(days=1)
            ),
            "date_range_to": str(datetime.datetime.utcnow()),
            "geo_file": {
                "type": "test",
                "geometry": {"type": "test", "coordinates": [[[[22.33, 44.55]]]]},
            },
        },
    )
    assert response.status_code == fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "request_data",
    [
        {
            "name": "test",
            "description": "desc",
            "date_range_from": str(datetime.datetime.utcnow()),
            "date_range_to": str(datetime.datetime.utcnow()),
            "geo_file": {
                "type": "test",
                "geometry": {"type": "test", "coordinates": [[[[22.33, 44.55]]]]},
            },
        },
        {
            "name": "test",
            "date_range_from": str(datetime.datetime.utcnow()),
            "date_range_to": str(datetime.datetime.utcnow()),
            "geo_file": {
                "type": "test",
                "geometry": {"type": "test", "coordinates": [[[[22.33, 44.55]]]]},
            },
        },
    ],
)
def test_successful_create_project(request_data):
    client = TestClient(backend_app)
    response = client.post("/api/projects", json=request_data)
    assert response.status_code == fastapi.status.HTTP_200_OK
    response = client.get("/api/projects")
    assert len(response.json()) == 1


def test_successful_update_project():
    # given
    client = TestClient(backend_app)
    project_name = "TESTEM JESTEM"
    data = {
        "name": project_name,
        "description": "desc",
        "date_range_from": str(datetime.datetime.utcnow()),
        "date_range_to": str(datetime.datetime.utcnow()),
        "geo_file": {
            "type": "test",
            "geometry": {"type": "test", "coordinates": [[[[22.33, 44.55]]]]},
        },
    }

    response = client.post("/api/projects", json=data)
    assert response.status_code == fastapi.status.HTTP_200_OK
    created_project = response.json()

    # when
    response = client.put(
        f"/api/projects/{created_project['id']}",
        json={
            "name": project_name,
            "description": "other_description",
            "date_range_from": str(datetime.datetime.utcnow()),
            "date_range_to": str(datetime.datetime.utcnow()),
            "geo_file": {
                "type": "test",
                "geometry": {"type": "test", "coordinates": [[[[22.33, 44.55]]]]},
            },
        },
    )
    assert response.status_code == fastapi.status.HTTP_200_OK

    # then
    response = client.get(f"/api/projects/{created_project['id']}")
    assert response.json()["description"] == "other_description"
