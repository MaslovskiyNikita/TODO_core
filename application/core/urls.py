from api.v1.projects.views.projects import ProjectViewSet
from api.v1.tasks.views.tasks_views import TaskViews
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("tasks", TaskViews)

urlpatterns = [
    path("", include(router.urls)),
]
