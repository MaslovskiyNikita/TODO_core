from core.celery_core import app
from core.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from projects.models.project_model import Project


@app.task  # type: ignore[misc]
def invite_user_to_project(member_id, project_id) -> None:
    project = Project.objects.get(id=project_id)
    # user = User.objects.get(id=member_id)
    send_mail(
        f"Invite to project {project.name}",
        f"{project.owner} want you to invite this project {project.name}",
        EMAIL_HOST_USER,
        "nikitamaslovskiy999@gmail.com",  # [user.email],
        fail_silently=False,
    )
