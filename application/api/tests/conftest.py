import uuid

import pytest
from auth.choices.roles import Role
from auth.jwt_service.jwt_code import JWTGenerator
from core.settings import ALGORITMS, SECRET_KEY
from dotenv import load_dotenv
from projects.factories.project import ProjectFactory
from projects.factories.project_member import ProjectMemberFactory
from rest_framework.test import APIClient
from tasks.factories.task import TaskFactory

load_dotenv()


@pytest.fixture()
def project():
    return ProjectFactory.create()


@pytest.fixture
def task():
    return TaskFactory.create()


@pytest.fixture
def project_member():
    return ProjectMemberFactory.create()


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture
def payload_base():
    return {
        "sub": "1234567890",
        "name": "John Doe",
        "uuid": str(uuid.uuid4()),
        "role": Role.USER.value,
        "permissions": [],
    }


@pytest.fixture
def payload_admin(payload_base, project_member):
    payload_base["uuid"] = project_member.user
    payload_base["role"] = Role.ADMIN.value
    return payload_base


@pytest.fixture
def payload_user(payload_base):
    payload_base["permissions"] = []
    return payload_base


@pytest.fixture
def payload_owner(payload_base, project):
    payload_base["uuid"] = project.owner
    payload_base["permissions"] = [
        "project_create",
        "task_create",
        "project_read",
        "task_read",
        "project_update",
        "task_update",
        "project_delete",
        "task_delete",
    ]
    return payload_base


@pytest.fixture()
def client_admin(client, payload_admin):
    token_admin = JWTGenerator(SECRET_KEY, ALGORITMS).jwt_code(payload_admin)
    client.credentials(HTTP_AUTHORIZATION=("Bearer " + token_admin))
    return client


@pytest.fixture()
def client_user(client, payload_user):
    token_user = JWTGenerator(SECRET_KEY, ALGORITMS).jwt_code(payload_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_user}")
    return client


@pytest.fixture()
def client_owner(client, payload_owner):
    token_owner = JWTGenerator(SECRET_KEY, ALGORITMS).jwt_code(payload_owner)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_owner}")
    return client
