import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status",
    [
        ("client_admin", status.HTTP_200_OK),
        ("client_user", status.HTTP_404_NOT_FOUND),
        ("client_owner", status.HTTP_200_OK),
    ],
)
def test_update_project(
    project: Project,
    client_fixture_name: str,
    expected_status: int,
    request: pytest.FixtureRequest,
):

    client = request.getfixturevalue(client_fixture_name)

    update_data = {
        "name": "Updated Test Project",
        "description": "Updated project description",
        "owner": str(project.owner),
    }

    response = client.put(
        f"/api/v1/projects/{project.id}/", data=update_data, format="json"
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        updated_project = Project.objects.get(id=project.id)
        assert updated_project.name == update_data["name"]
        assert updated_project.description == update_data["description"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status",
    [
        ("client_admin", status.HTTP_400_BAD_REQUEST),
        ("client_user", status.HTTP_404_NOT_FOUND),
        ("client_owner", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_failed_update_project(
    project: Project,
    client_fixture_name: str,
    expected_status: int,
    request: pytest.FixtureRequest,
):

    client = request.getfixturevalue(client_fixture_name)

    response = client.put(f"/api/v1/projects/{project.id}/", data={}, format="json")

    assert response.status_code == expected_status
