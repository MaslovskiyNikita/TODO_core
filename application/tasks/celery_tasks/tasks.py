import json
from datetime import timedelta

from auth.requsts_to_auth.users_mail import UserManagementClient
from aws.ses_manager import ses_manager
from aws.templates.deadline_notification import deadline_template_data
from celery import shared_task
from core.settings import EMAIL_HOST_USER
from django.db.models import Prefetch
from django.utils import timezone
from tasks.models import Task, TaskSubscriber


@shared_task
def check_deadline():
    now = timezone.now()
    time_threshold = now + timedelta(hours=1)

    tasks = Task.objects.filter(
        due_date__gte=now,
        due_date__lte=time_threshold,
        notification_sent=False,
        due_date__isnull=False,
    )

    for task in tasks:
        send_deadline_notification.delay(str(task.id))
        task.notification_sent = True
        task.save()


@shared_task
def send_deadline_notification(task_id):
    task = Task.objects.prefetch_related("subscribers").get(id=task_id)

    users_email = UserManagementClient().get_users_email()  # task.subscribers.user.mail

    for subscriber in task.subscribers.all():

        template_data = deadline_template_data(task)

        ses_manager.send_templated_email(
            source=EMAIL_HOST_USER,
            destination=users_email,  # subscriber.user.email
            template_name="DeadlineNotificationTemplate",
            template_data=template_data,
        )
