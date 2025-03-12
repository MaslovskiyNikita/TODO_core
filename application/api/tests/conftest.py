import pytest
from api.tests.e2e.payload_for_tests import payload_admin, payload_owner, payload_user
from auth.jwt_service.jwt_code import JWTGenerator
from core.settings import ALGORITMS, SECRET_KEY
from dotenv import load_dotenv
from projects.factories.project import ProjectFactory
from rest_framework.test import APIClient
from tasks.factories.task import TaskFactory

load_dotenv()


@pytest.fixture
def project():
    return ProjectFactory.create()


@pytest.fixture
def task():
    return TaskFactory.create()


@pytest.fixture()
def client_admin():
    token_admin = JWTGenerator(SECRET_KEY, ALGORITMS).jwt_code(payload_admin)
    client_admin = APIClient()
    client_admin.credentials(HTTP_AUTHORIZATION=("Bearer " + token_admin))
    return client_admin


@pytest.fixture()
def client_user():
    token_user = JWTGenerator(SECRET_KEY, ALGORITMS).jwt_code(payload_user)
    client_user = APIClient()
    client_user.credentials(HTTP_AUTHORIZATION=f"Bearer {token_user}")
    return client_user


@pytest.fixture()
def client_owner():
    token_owner = JWTGenerator(SECRET_KEY, ALGORITMS).jwt_code(payload_owner)
    client_owner = APIClient()
    client_owner.credentials(HTTP_AUTHORIZATION=f"Bearer {token_owner}")
    return client_owner
