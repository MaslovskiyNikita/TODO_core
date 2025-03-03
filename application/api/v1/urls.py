from django.urls import include, path

urlpatterns = [
    path("tasks/", include("api.v1.tasks.urls")),
    path("projects/", include("api.v1.projects.urls")),
]
