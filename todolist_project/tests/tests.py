from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from todo_list.models import Task, Work
from rest_framework.authtoken.models import Token


User = get_user_model()


class TaskViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@yandex.ru')
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True, email='adminuser@yandex.ru')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.task = Task.objects.create(user=self.user, title='Test Task')

    def test_get_tasks(self):
        url = reverse('api:task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_detail(self):
        url = reverse('api:task-detail', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        url = reverse('api:task-list')
        data = {'title': 'New Task', 'description': 'New Description'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_task(self):
        url = reverse('api:task-detail', kwargs={'pk': self.task.pk})
        data = {'title': 'Updated Task'}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task(self):
        url = reverse('api:task-detail', kwargs={'pk': self.task.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permissions(self):
        url = reverse('api:task-list')
        data = {'title': 'New Task'}
        self.client.credentials()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class WorkStatusUpdateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@yandex.ru')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.task = Task.objects.create(user=self.user, title='Test Task')
        self.work = Work.objects.create(task=self.task, title='test job')

    def test_update_work_status(self):
        url = reverse('api:work_complete', kwargs={'pk': self.work.pk})
        data = {'completed': 'True'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.work.refresh_from_db()
        self.assertTrue(self.work.completed)
