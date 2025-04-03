from datetime import timedelta

import boto3
from aws.ses_manager import SesManager
from botocore.exceptions import ClientError
from celery import shared_task
from core.celery_core import app
from core.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.utils import timezone
from projects.models.project_model import Project
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
    try:
        task = Task.objects.get(id=task_id)
        subscribers = TaskSubscriber.objects.filter(task=task)
        ses_client = SesManager.get_ses_client()

        for subscriber in subscribers:
            subject = f'Напоминание: Дедлайн задачи "{task.title}"'
            message = f"""
            Задача "{task.title}" приближается к дедлайну!
            Осталось времени: 1 час
            Описание: {task.description}
            Проект: {task.project.title}
            """
            try:
                ses_client.send_email(
                    Source=EMAIL_HOST_USER,
                    Destination={
                        "ToAddresses": ["nikitamaslovskiy999@gmail.com"]
                    },  # user.mail
                    Message={
                        "Subject": {"Data": subject},
                        "Body": {"Text": {"Data": message}},
                    },
                )
            except ClientError as e:
                print(f"SES Error: {e.response['Error']['Message']}")

    except Exception as e:
        print(f"Ошибка отправки уведомления: {e}")
