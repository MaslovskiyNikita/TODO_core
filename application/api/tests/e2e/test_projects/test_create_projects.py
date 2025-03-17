import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status",
    [
        ("client_admin", status.HTTP_201_CREATED),
        ("client_user", status.HTTP_201_CREATED),
        ("client_owner", status.HTTP_201_CREATED),
    ],
)
def test_create_project(
    client_fixture_name: str, expected_status: int, request: pytest.FixtureRequest
):
    client = request.getfixturevalue(client_fixture_name)
    data = {"name": "Test", "description": "This is for tests"}
    response = client.post("/api/v1/projects/", data=data)
    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        project_id = response.json().get("id")
        assert Project.objects.filter(id=project_id).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status",
    [
        ("client_admin", status.HTTP_400_BAD_REQUEST),
        ("client_user", status.HTTP_400_BAD_REQUEST),
        ("client_owner", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_failed_create_project(
    client_fixture_name: str, expected_status: int, request: pytest.FixtureRequest
):
    client = request.getfixturevalue(client_fixture_name)
    data: dict = {}
    response = client.post("/api/v1/projects/", data=data)
    assert response.status_code == expected_status
