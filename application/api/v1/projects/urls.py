from api.v1.projects.views.projects import ProjectViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", ProjectViewSet, basename="projects")

urlpatterns = router.urls
