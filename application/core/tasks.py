from datetime import timedelta

from celery import shared_task
from core.celery_core import app
from core.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.utils import timezone
from projects.models.project_model import Project
from tasks.models import Task, TaskSubscriber


@shared_task(name="check_deadline")
def check_deadline():
    now = timezone.now()
    time_threshold = now + timedelta(hours=1)

    tasks = Task.objects.filter(
        due_date__gte=now, due_date__lte=time_threshold, notification_sent=False
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

        for subscriber in subscribers:
            # user = User.objects.get(id=subscriber.user) Надо будет брать из таблицы юзеров эмаил
            subject = f'Напоминание: Дедлайн задачи "{task.title}"'
            message = f"""
            Задача "{task.title}" приближается к дедлайну!
            Осталось времени: 1 час
            Описание: {task.description}
            Проект: {task.project.title}
            """
            send_mail(
                subject,
                message,
                EMAIL_HOST_USER,
                "nikitamaslovskiy999@gmail.com",  # [user.email],
                fail_silently=False,
            )
    except Exception as e:
        print(f"Ошибка отправки уведомления: {e}")
