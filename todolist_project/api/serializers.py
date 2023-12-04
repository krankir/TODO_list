import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from todo_list.models import Task, Work

User = get_user_model()


class WorkSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с работами в задачах."""

    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Work
        fields = ['id', 'title', 'completed', 'due_date', 'user']

    def update(self, instance, validated_data):
        if self.context['request'].auth.user_id != instance.task.user_id:
            raise ValidationError({
                'Authorization problem': 'У вас недостаточно прав для закрытия задачи'
            })
        if validated_data['completed'] is True:
            validated_data.update({'due_date': datetime.datetime.utcnow()})
        elif validated_data['completed'] is False:
            validated_data.update({'due_date': None})
        instance.title = validated_data.get('title', instance.title)
        instance.completed = validated_data.get('completed',
                                                instance.completed)
        instance.due_date = validated_data.get('due_date', instance.due_date)

        instance.save()
        return instance


class TaskReedSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения задач."""

    works = WorkSerializer(many=True, source='work_set')

    class Meta:
        model = Task
        fields = ('id', 'title', 'created_date', 'user', 'works', )


class TaskWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания задач."""

    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ('title', 'user',)


