from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, status
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from api.permissions import IsAdminOrAuthor
from api.serializers import (
    WorkSerializer, TaskReedSerializer, TaskWriteSerializer
)
from todo_list.models import Task, Work

User = get_user_model()


class TaskViewSet(viewsets.ModelViewSet):
    """Представление для отображения задач."""

    queryset = Task.objects.all().select_related('task')
    permission_classes = (IsAdminOrAuthor,)

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username:
            if not self.request.auth.user.is_staff:
                return Task.objects.none()
            return Task.objects.filter(user__username=username)

        return Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TaskReedSerializer
        return TaskWriteSerializer

    def destroy(self, request, *args, **kwargs):
        pk = int(self.kwargs.get('pk'))
        user = self.request.user.id

        instance = Task.objects.get(id=pk)
        if instance:
            if instance.user_id == user:
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'У вас недостаточно прав для удаление этой записи'},
                        status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.delete()


class WorkStatusUpdate(generics.UpdateAPIView):
    """Представление для закрытия работы."""

    name = 'work_complete'
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

