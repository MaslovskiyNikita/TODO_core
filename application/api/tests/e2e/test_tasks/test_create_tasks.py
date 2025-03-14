import datetime
import uuid

import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project
from rest_framework import status
from tasks.models import Task


@pytest.mark.django_db
class TestCreateTaskAPI:
    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_201_CREATED),
            (client_user, status.HTTP_201_CREATED),
            (client_owner, status.HTTP_201_CREATED),
        ],
    )
    def test_create_task(
        self, project: Project, client_fixture, expected_status, request
    ):
        client = request.getfixturevalue(client_fixture.__name__)
        data = {
            "title": "Task test",
            "description": "Task description",
            "status": "asdasd",
            "due_date": datetime.datetime.now().isoformat(),
            "project": project.id,
            "owner": str(uuid.uuid4()),
            "assigned_to": str(uuid.uuid4()),
        }
        response = client.post("/api/v1/tasks/", data=data)
        assert response.status_code == expected_status

        if expected_status == status.HTTP_201_CREATED:
            task_id = response.json().get("id")
            assert Task.objects.filter(id=task_id).exists()

    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_400_BAD_REQUEST),
            (client_user, status.HTTP_400_BAD_REQUEST),
            (client_owner, status.HTTP_400_BAD_REQUEST),
        ],
    )
    def test_failed_create_task(self, client_fixture, expected_status, request):
        client = request.getfixturevalue(client_fixture.__name__)
        data: dict = {}
        response = client.post("/api/v1/tasks/", data=data)
        assert response.status_code == expected_status
