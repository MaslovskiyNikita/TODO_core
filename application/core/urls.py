from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("api/", include("api.urls")),
]
