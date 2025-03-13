import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project
from rest_framework import status


@pytest.mark.django_db
class TestDeleteProjectAPI:
    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_204_NO_CONTENT),
            (client_user, status.HTTP_404_NOT_FOUND),
            (client_owner, status.HTTP_404_NOT_FOUND),
        ],
    )
    def test_delete_project(
        self, project: Project, client_fixture, expected_status, request
    ):
        client = request.getfixturevalue(client_fixture.__name__)
        response = client.delete(f"/api/v1/projects/{project.id}/")
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_404_NOT_FOUND),
            (client_user, status.HTTP_404_NOT_FOUND),
            (client_owner, status.HTTP_404_NOT_FOUND),
        ],
    )
    def test_failed_delete_project(self, client_fixture, expected_status, request):
        client = request.getfixturevalue(client_fixture.__name__)
        response = client.delete("/api/v1/projects/aaa/")
        assert response.status_code == expected_status
