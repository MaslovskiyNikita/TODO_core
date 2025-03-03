from api.v1.tasks.views.tasks_views import TaskViews
from django.urls import include, path
from rest_framework.routers import DefaultRouter

task_router = DefaultRouter()
task_router.register("", TaskViews, basename="tasks")


urlpatterns = task_router.urls
