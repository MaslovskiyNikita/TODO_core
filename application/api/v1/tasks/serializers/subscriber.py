from rest_framework import serializers
from tasks.models.task_model import Subscriber


class TaskSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ("user", "task")
