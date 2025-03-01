import django_filters
from tasks.models.task_model import Task


class TaskFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = Task
        fields = ["title", "status"]
