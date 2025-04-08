from auth.requsts_to_auth.users_mail import UserManagementClient
from aws.ses_manager import ses_manager
from aws.templates.project_invitation import project_invitation_template
from celery import shared_task
from core.celery_core import app
from core.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


@shared_task  # type: ignore[misc]
def send_project_invitation_email(member_id, project_name, project_owner) -> None:

    template_data = project_invitation_template(
        project_name=project_name, project_owner=project_owner
    )

    user_email = UserManagementClient().get_users_email(member_id)

    ses_manager.send_templated_email(
        source=EMAIL_HOST_USER,
        destination=user_email,
        template_name="InviteNotificationTemplate",
        template_data=template_data,
    )
