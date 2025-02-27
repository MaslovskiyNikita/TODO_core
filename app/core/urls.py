from django.urls import include, path
from projects.views.projects_views import ProjectViewSet
from rest_framework.routers import DefaultRouter
from tasks.views.tasks_views import TaskViews

router = DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("tasks", TaskViews)

urlpatterns = [
    path("", include(router.urls)),
]
