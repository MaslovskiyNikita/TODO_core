from aws.ses_manager import ses_manager
from aws.templates.status_notification import status_template
from celery import shared_task
from core.settings import EMAIL_HOST_USER


@shared_task
def send_new_status(task_name, task_owner):

    template_data = status_template(task_name, task_owner)
    ses_manager.send_templated_email(
        source=EMAIL_HOST_USER,
        destination=EMAIL_HOST_USER,  # subscriber.user.email
        template_name="DeadlineNotificationTemplate",
        template_data=template_data,
    )
