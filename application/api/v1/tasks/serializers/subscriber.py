from rest_framework import serializers
from tasks.models.task_model import TaskSubscriber


class TaskSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSubscriber
        fields = ("user", "task")
