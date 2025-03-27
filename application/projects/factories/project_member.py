import random
import uuid

import factory
from factory import Faker
from projects.factories.project import ProjectFactory
from projects.models import ProjectMember


class ProjectMemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectMember

    id = Faker("uuid4")
    project = factory.SubFactory(ProjectFactory)
    user = str(uuid.uuid4())
    role = "redactor"
