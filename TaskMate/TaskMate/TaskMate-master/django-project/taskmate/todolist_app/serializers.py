from rest_framework import serializers
from .models import TaskList

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        fields = ['id', 'manager', 'task', 'done']  
