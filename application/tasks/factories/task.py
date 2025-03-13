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
    owner = "7cbff8ff-41c7-48ef-b962-99cc6db81593"
    assigned_to = Faker("uuid4")
