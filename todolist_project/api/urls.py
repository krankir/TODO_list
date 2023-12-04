from django.template.defaulttags import url
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import TaskViewSet, WorkStatusUpdate

app_name = 'api'

router = DefaultRouter()
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/work_complete/<int:pk>/', WorkStatusUpdate.as_view(), name='work_complete'),
    path('v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
