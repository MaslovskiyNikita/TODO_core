import uuid

import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project
from rest_framework import status


@pytest.mark.django_db
class TestCreateMemberProjectAPI:
    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_201_CREATED),
        ],
    )
    def test_add_member_project(
        self, client_fixture, expected_status, request, project
    ):
        client = request.getfixturevalue(client_fixture.__name__)
        data = {"user": str(uuid.uuid4()), "role": "user"}
        response = client.post(
            f"/api/v1/projects/{project.id}/add_user_to_project/", data=data
        )
        assert response.status_code == expected_status

        assert expected_status == status.HTTP_201_CREATED

    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            (client_admin, status.HTTP_400_BAD_REQUEST),
            (client_user, status.HTTP_404_NOT_FOUND),
            (client_owner, status.HTTP_404_NOT_FOUND),
        ],
    )
    def test_failed_add_member_project(
        self, client_fixture, expected_status, request, project
    ):
        client = request.getfixturevalue(client_fixture.__name__)
        data: dict = {}
        response = client.post(
            f"/api/v1/projects/{project.id}/add_user_to_project/", data=data
        )
        assert response.status_code == expected_status
