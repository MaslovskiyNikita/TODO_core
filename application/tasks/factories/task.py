import factory
from factory import Faker
from projects.factories.project import ProjectFactory
from tasks.models import Task


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    id = Faker("uuid4")
    title = Faker("sentence", nb_words=5)
    description = Faker("sentence")
    status = Faker("word")
    due_date = Faker("date_time")
    project = factory.SubFactory(ProjectFactory)
    owner = Faker("uuid4")
    assigned_to = Faker("uuid4")
