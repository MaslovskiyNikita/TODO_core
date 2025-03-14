import datetime
import uuid

import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project
from rest_framework import status
from tasks.models import Task


@pytest.mark.django_db
class TestUpdateTaskAPI:
    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_200_OK),
            (client_user, status.HTTP_404_NOT_FOUND),
            (client_owner, status.HTTP_200_OK),
        ],
    )
    def test_update_task(
        self, task: Task, project: Project, client_fixture, expected_status, request
    ):
        client = request.getfixturevalue(client_fixture.__name__)
        data = {
            "title": "Task test",
            "description": "Task description",
            "status": "prikol",
            "due_date": datetime.datetime.now().isoformat(),
            "project": project.id,
            "owner": str(uuid.uuid4()),
            "assigned_to": str(uuid.uuid4()),
        }
        response = client.put(f"/api/v1/tasks/{task.id}/", data=data)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_404_NOT_FOUND),
            (client_user, status.HTTP_404_NOT_FOUND),
            (client_owner, status.HTTP_404_NOT_FOUND),
        ],
    )
    def test_failed_update_task(self, client_fixture, expected_status, request):
        client = request.getfixturevalue(client_fixture.__name__)
        data: dict = {}
        response = client.put("/api/v1/tasks/aaa/", data=data)
        assert response.status_code == expected_status
