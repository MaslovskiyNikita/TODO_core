import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from rest_framework import status
from tasks.models import Task


@pytest.mark.django_db
class TestTaskAPI:
    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_200_OK),
            (client_user, status.HTTP_200_OK),
            (client_owner, status.HTTP_200_OK),
        ],
    )
    def test_get_tasks(self, task: Task, client_fixture, expected_status, request):
        client = request.getfixturevalue(client_fixture.__name__)
        response = client.get("/api/v1/tasks/")
        assert response.status_code == expected_status
        assert isinstance(response.json().get("results"), list)

    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_200_OK),
            (client_user, status.HTTP_404_NOT_FOUND),
            (client_owner, status.HTTP_200_OK),
        ],
    )
    def test_get_task_by_id(self, task: Task, client_fixture, expected_status, request):
        client = request.getfixturevalue(client_fixture.__name__)
        response = client.get(f"/api/v1/tasks/{task.id}/")
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_404_NOT_FOUND),
            (client_user, status.HTTP_404_NOT_FOUND),
            (client_owner, status.HTTP_404_NOT_FOUND),
        ],
    )
    def test_failed_get_task_by_id(self, client_fixture, expected_status, request):
        client = request.getfixturevalue(client_fixture.__name__)
        response = client.get("/api/v1/tasks/aaa/")
        assert response.status_code == expected_status
