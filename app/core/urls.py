from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProjectMemberViewSet, ProjectViewSet, SubscriberViewSet, TaskViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("tasks", TaskViewSet)
router.register("project_members", ProjectMemberViewSet)
router.register("subscribers", SubscriberViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
