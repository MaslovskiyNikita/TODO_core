import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status",
    [
        ("client_admin", status.HTTP_204_NO_CONTENT),
        ("client_user", status.HTTP_404_NOT_FOUND),
        ("client_owner", status.HTTP_204_NO_CONTENT),
    ],
)
def test_delete_project(
    project: Project,
    client_fixture_name: str,
    expected_status: int,
    request: pytest.FixtureRequest,
):
    client = request.getfixturevalue(client_fixture_name)
    response = client.delete(f"/api/v1/projects/{project.id}/")
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status",
    [
        ("client_admin", status.HTTP_404_NOT_FOUND),
        ("client_user", status.HTTP_404_NOT_FOUND),
        ("client_owner", status.HTTP_404_NOT_FOUND),
    ],
)
def test_failed_delete_project(
    client_fixture_name: str, expected_status: int, request: pytest.FixtureRequest
):
    client = request.getfixturevalue(client_fixture_name)
    response = client.delete("/api/v1/projects/aaa/")
    assert response.status_code == expected_status
