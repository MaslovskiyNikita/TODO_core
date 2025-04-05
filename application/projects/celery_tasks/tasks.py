from aws.ses_manager import ses_manager
from aws.templates.project_invitation import project_invitation_template
from botocore.exceptions import ClientError
from celery import shared_task
from core.celery_core import app
from core.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from projects.models.project_model import Project


@shared_task  # type: ignore[misc]
def send_project_invitation_email(member_id, project_name, project_owner) -> None:

    template_data = project_invitation_template(
        project_name=project_name, project_owner=project_owner
    )

    ses_manager.send_templated_email(
        source=EMAIL_HOST_USER,
        destination=EMAIL_HOST_USER,
        template_name="InviteNotificationTemplate",
        template_data=template_data,
    )
