from api.v1.projects.views.projects import ProjectViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter, SimpleRouter

router = SimpleRouter()
router.register("", ProjectViewSet, basename="projects")


# projects_router = NestedSimpleRouter(router, r'projects', lookup='project')

# projects_router.register(
#     r'projects/(?P<project_pk>[^/.]+)/members',
#     ProjectMembersViewSet,
#     basename='project-members'
# )

# urlpatterns = [
#     path('', include(router.urls)),
# ]
urlpatterns = router.urls
