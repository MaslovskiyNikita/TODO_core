import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project
from rest_framework import status


@pytest.mark.django_db
class TestUpdateProjectAPI:
    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_200_OK),
            (client_user, status.HTTP_404_NOT_FOUND),
            (client_owner, status.HTTP_404_NOT_FOUND),
        ],
    )
    def test_update_project(
        self, project: Project, client_fixture, expected_status, request
    ):
        client = request.getfixturevalue(client_fixture.__name__)
        data = {
            "name": "Updated Test",
            "description": "This is an updated test",
            "owner": project.owner,
        }
        response = client.put(
            f"/api/v1/projects/{project.id}/", data=data, format="json"
        )
        assert response.status_code == expected_status

        if expected_status == status.HTTP_200_OK:
            updated_project = Project.objects.get(id=project.id)
            assert updated_project.name == data["name"]
            assert updated_project.description == data["description"]

    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_400_BAD_REQUEST),
            (client_user, status.HTTP_404_NOT_FOUND),
            (client_owner, status.HTTP_404_NOT_FOUND),
        ],
    )
    def test_failed_update_project(
        self, project: Project, client_fixture, expected_status, request
    ):
        client = request.getfixturevalue(client_fixture.__name__)
        data: dict = {}
        response = client.put(
            f"/api/v1/projects/{project.id}/", data=data, format="json"
        )
        assert response.status_code == expected_status
