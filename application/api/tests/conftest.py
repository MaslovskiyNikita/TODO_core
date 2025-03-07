import pytest
from projects.factories.project import ProjectFactory
from rest_framework.test import APIClient
from tasks.factories.task import TaskFactory


@pytest.fixture
def project():
    return ProjectFactory.create()


@pytest.fixture
def task():
    return TaskFactory.create()


@pytest.fixture(scope="session")
def headers():
    return "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwidXVpZCI6IjNmNDdmNzg2LTgyNDAtNDZhYi1hZGNmLWVlMmY1NGQwNThkNyIsInJvbGUiOiJhZG1pbiIsInBlcm1pc3Npb25zIjpbInByb2plY3RfY3JlYXRlIiwidGFza19jcmVhdGUiLCJwcm9qZWN0X3JlYWQiLCJ0YXNrX3JlYWQiLCJwcm9qZWN0X3VwZGF0ZSIsInRhc2tfdXBkYXRlIiwicHJvamVjdF9kZXN0cm95IiwidGFza19kZXN0cm95Il19.cc-he7ggEVkEzUevx6zWgDLVHD92i5LEDbBrOULT8Sc"


@pytest.fixture(scope="session")
def client(headers):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=headers)
    return client
