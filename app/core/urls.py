from django.urls import include, path
from projects.views import ProjectViewSet
from rest_framework.routers import DefaultRouter
from tasks.views import TaskListCreate

router = DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("tasks", TaskListCreate)

urlpatterns = [
    path("", include(router.urls)),
]
