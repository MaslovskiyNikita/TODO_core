from aws.ses_manager import SesManager
from botocore.exceptions import ClientError
from celery import shared_task
from core.celery_core import app
from core.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from projects.models.project_model import Project


@shared_task  # type: ignore[misc]
def send_project_invitation_email(member_id, project_name, project_owner) -> None:
    ses_client = SesManager.get_ses_client()

    try:

        ses_client.send_email(
            Source=EMAIL_HOST_USER,
            Destination={"ToAddresses": ["nikitamaslovskiy999@gmail.com"]},  # user.mail
            Message={
                "Subject": {"Data": f"Invite to project {project_name}"},
                "Body": {
                    "Text": {
                        "Data": f"{project_owner} want you to invite this project {project_name}"
                    }
                },
            },
        )
    except ClientError as e:
        print(f"SES Error: {e.response['Error']['Message']}")
