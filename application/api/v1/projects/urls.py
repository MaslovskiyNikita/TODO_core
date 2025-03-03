from api.v1.projects.views.projects import ProjectViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

project_router = DefaultRouter()
project_router.register("", ProjectViewSet, basename="projects")

urlpatterns = project_router.urls
