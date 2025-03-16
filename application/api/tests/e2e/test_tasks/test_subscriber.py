import datetime
import uuid

import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from rest_framework import status
from tasks.models import Task


@pytest.mark.django_db
class TestSubscriberTaskAPI:
    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_201_CREATED),
        ],
    )
    def test_create_subscriber(self, task, client_fixture, expected_status, request):
        client = request.getfixturevalue(client_fixture.__name__)
        data = {"user": str(uuid.uuid4())}
        response = client.post(f"/api/v1/tasks/{task.id}/subscribe_on_task/", data=data)
        assert response.status_code == expected_status

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
