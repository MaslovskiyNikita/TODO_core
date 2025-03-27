import uuid

import factory
from factory import Faker
from projects.models import Project


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    id = Faker("uuid4")
    name = Faker("sentence")
    description = Faker("sentence")
    owner = str(uuid.uuid4())
