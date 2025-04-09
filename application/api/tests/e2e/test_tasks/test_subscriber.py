import uuid

import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from rest_framework import status
from tasks.models import Task


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status",
    [
        ("client_admin", status.HTTP_201_CREATED),
    ],
)
def test_create_subscriber(
    task: Task,
    client_fixture_name: str,
    expected_status: int,
    request: pytest.FixtureRequest,
):
    client = request.getfixturevalue(client_fixture_name)
    data = {"user": str(uuid.uuid4())}
    response = client.post(
        f"/api/v1/tasks/{task.id}/subscribers/", data=data, format="json"
    )
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status",
    [
        ("client_admin", status.HTTP_400_BAD_REQUEST),
        ("client_user", status.HTTP_400_BAD_REQUEST),
        ("client_owner", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_failed_create_task(
    client_fixture_name: str, expected_status: int, request: pytest.FixtureRequest
):
    client = request.getfixturevalue(client_fixture_name)
    data: dict = {}
    response = client.post("/api/v1/tasks/", data=data, format="json")
    assert response.status_code == expected_status
