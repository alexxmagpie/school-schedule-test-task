from datetime import datetime

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.course.models import Schedule
from apps.course.api.serializers import ScheduleSerializer

from asgiref.sync import sync_to_async

from adrf.views import APIView


class ScheduleAPIView(APIView):
    """
    GET: /api/schedule/
    """
    async def get(self, request, *args, **kwargs):
        for_today = request.query_params.get('for_today', 'false').lower() == 'true'
        class_name = request.query_params.get('class_name')

        if for_today is False and class_name is None:
            cache_key = 'schedules_all'
        else:
            cache_key = f'schedules_{for_today}_{class_name}'

        cached_response = cache.get(cache_key)

        if cached_response:
            return Response(cached_response, status=status.HTTP_200_OK)

        schedules = await self.get_schedules(for_today, class_name)
        serializer = await self.serialize_schedules(schedules)

        response_data = await serializer.adata

        cache.set(cache_key, response_data, timeout=60*3)

        return Response(response_data, status=status.HTTP_200_OK)

    @sync_to_async
    def get_schedules(self, for_today, class_name):
        schedules = Schedule.objects.select_related('course', 'subject', 'teacher')
        if for_today and class_name:
            today = datetime.today().weekday()
            schedules = schedules.filter(day_of_week=today, course__name=class_name)
        elif for_today:
            today = datetime.today().weekday()
            schedules = schedules.filter(day_of_week=today)
        elif class_name:
            schedules = schedules.filter(course__name=class_name)

        return schedules.order_by('day_of_week', 'start_time')

    @sync_to_async
    def serialize_schedules(self, schedules):
        return ScheduleSerializer(schedules, many=True)
