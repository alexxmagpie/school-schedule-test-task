from django.urls import path

from apps.course.api.views import ScheduleAPIView


urlpatterns = [
    path('schedule/', ScheduleAPIView.as_view(), name='schedule'),
]
