from django.urls import include, path
from projects.views.views_projects import ProjectViewSet
from rest_framework.routers import DefaultRouter
from tasks.views.views_tasks import TaskListCreate

router = DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("tasks", TaskListCreate)

urlpatterns = [
    path("", include(router.urls)),
]
