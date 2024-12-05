# pylint: disable=R0903

import asyncio

from datetime import datetime

from unittest.mock import patch, MagicMock

import pytest

from asgiref.sync import sync_to_async

from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework import status
from rest_framework.test import APIRequestFactory

from apps.course.factories import CourseFactory, ScheduleFactory

from apps.course.api.views import ScheduleAPIView
from apps.course.api.serializers import CourseSerializer, ScheduleSerializer

from apps.student.factories import StudentFactory


User = get_user_model()


@pytest.mark.django_db
@pytest.mark.asyncio
class TestScheduleAPIView:
    @pytest.fixture
    def request_factory(self):
        return APIRequestFactory()

    @pytest.fixture
    def view(self):
        return ScheduleAPIView.as_view()

    @pytest.fixture
    def schedule_factory(self):
        return ScheduleFactory

    async def test_get_all_schedules_cached(self, request_factory, view, schedule_factory):
        sample_data = await sync_to_async(schedule_factory.create)()
        request = request_factory.get('/api/schedule/')
        response_data = [{
            'course': {
                'name': sample_data.course.name,
                'students_count': 0
            },
            'subject': {
                'name': sample_data.subject.name
            },
            'teacher': {
                'name': sample_data.teacher.name
            },
            'day_of_week': sample_data.day_of_week,
            'start_time': sample_data.start_time.strftime("%H:%M"),
        }]

        cache_key = 'schedules_all'
        cache.set(cache_key, response_data, timeout=60*3)

        response = await view(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == response_data

    async def test_get_today_schedules_cached(self, request_factory, view, schedule_factory):
        sample_data = await sync_to_async(schedule_factory.create)(day_of_week=datetime.today().strftime('%A'))
        request = request_factory.get('/api/schedule/', {'for_today': 'true'})
        response_data = [{
            'course': {
                'name': sample_data.course.name,
                'students_count': 0
            },
            'subject': {
                'name': sample_data.subject.name
            },
            'teacher': {
                'name': sample_data.teacher.name
            },
            'day_of_week': sample_data.day_of_week,
            'start_time': sample_data.start_time.strftime("%H:%M"),
        }]

        cache_key = 'schedules_True_None'
        cache.set(cache_key, response_data, timeout=60*3)

        response = await view(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == response_data

    async def test_get_class_schedules_cached(self, request_factory, view, schedule_factory):
        sample_data = await sync_to_async(schedule_factory.create)(course__name='TEST_COURSE')
        request = request_factory.get('/api/schedule/', {'class_name': sample_data.course.name})
        response_data = [{
            'course': {
                'name': sample_data.course.name,
                'students_count': 0
            },
            'subject': {
                'name': sample_data.subject.name
            },
            'teacher': {
                'name': sample_data.teacher.name
            },
            'day_of_week': sample_data.day_of_week,
            'start_time': sample_data.start_time.strftime("%H:%M"),
        }]

        cache_key = f'schedules_False_{sample_data.course.name}'
        cache.set(cache_key, response_data, timeout=60*3)

        response = await view(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == response_data

    async def test_get_today_class_schedules_cached(self, request_factory, view, schedule_factory):
        sample_data = await sync_to_async(schedule_factory.create)(
            course__name='TEST_COURSE', day_of_week=datetime.today().strftime('%A'))
        request = request_factory.get('/api/schedule/', {'for_today': 'true', 'class_name': sample_data.course.name})
        response_data = [{
            'course': {
                'name': sample_data.course.name,
                'students_count': 0
            },
            'subject': {
                'name': sample_data.subject.name
            },
            'teacher': {
                'name': sample_data.teacher.name
            },
            'day_of_week': sample_data.day_of_week,
            'start_time': sample_data.start_time.strftime("%H:%M"),
        }]

        cache_key = f'schedules_True_{sample_data.course.name}'
        cache.set(cache_key, response_data, timeout=60*3)

        response = await view(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == response_data

    async def test_get_all_schedules_not_cached(self, request_factory, view, schedule_factory):
        sample_data = await sync_to_async(schedule_factory.create)()
        request = request_factory.get('/api/schedule/')

        cache_key = 'schedules_all'
        cache.delete(cache_key)

        with patch('apps.course.api.views.ScheduleAPIView.get_schedules') as mock_get_schedules:
            with patch('apps.course.api.views.ScheduleAPIView.serialize_schedules') as mock_serialize_schedules:
                mock_get_schedules.return_value = asyncio.Future()
                mock_get_schedules.return_value.set_result([sample_data])

                mock_serializer_instance = MagicMock()
                mock_serializer_instance.adata = asyncio.Future()
                mock_serializer_instance.adata.set_result([{
                    'course': sample_data.course.name,
                    'subject': sample_data.subject.name,
                    'teacher': sample_data.teacher.name,
                    'day_of_week': sample_data.day_of_week,
                    'start_time': sample_data.start_time.strftime("%H:%M"),
                }])

                mock_serialize_schedules.return_value = mock_serializer_instance

                response = await view(request)

                assert response.status_code == status.HTTP_200_OK
                assert response.data == [{
                    'course': sample_data.course.name,
                    'subject': sample_data.subject.name,
                    'teacher': sample_data.teacher.name,
                    'day_of_week': sample_data.day_of_week,
                    'start_time': sample_data.start_time.strftime("%H:%M"),
                }]

    async def test_get_today_class_schedules_not_cached(self, request_factory, view, schedule_factory):
        sample_data = await sync_to_async(schedule_factory.create)(
            course__name='TEST_COURSE', day_of_week=datetime.today().strftime('%A'))
        request = request_factory.get('/api/schedule/', {'for_today': 'true', 'class_name': sample_data.course.name})

        cache_key = f'schedules_True_{sample_data.course.name}'
        cache.delete(cache_key)

        with patch('apps.course.api.views.ScheduleAPIView.get_schedules') as mock_get_schedules:
            with patch('apps.course.api.views.ScheduleAPIView.serialize_schedules') as mock_serialize_schedules:
                mock_get_schedules.return_value = asyncio.Future()
                mock_get_schedules.return_value.set_result([sample_data])

                mock_serializer_instance = MagicMock()
                mock_serializer_instance.adata = asyncio.Future()
                mock_serializer_instance.adata.set_result([{
                    'course': sample_data.course.name,
                    'subject': sample_data.subject.name,
                    'teacher': sample_data.teacher.name,
                    'day_of_week': sample_data.day_of_week,
                    'start_time': sample_data.start_time.strftime("%H:%M"),
                }])

                mock_serialize_schedules.return_value = mock_serializer_instance

                response = await view(request)

                assert response.status_code == status.HTTP_200_OK
                assert response.data == [{
                    'course': sample_data.course.name,
                    'subject': sample_data.subject.name,
                    'teacher': sample_data.teacher.name,
                    'day_of_week': sample_data.day_of_week,
                    'start_time': sample_data.start_time.strftime("%H:%M"),
                }]

    async def test_get_today_schedules_not_cached(self, request_factory, view, schedule_factory):
        sample_data = await sync_to_async(schedule_factory.create)(day_of_week=datetime.today().strftime('%A'))
        request = request_factory.get('/api/schedule/', {'for_today': 'true'})

        cache_key = 'schedules_True_None'
        cache.delete(cache_key)

        with patch('apps.course.api.views.ScheduleAPIView.get_schedules') as mock_get_schedules:
            with patch('apps.course.api.views.ScheduleAPIView.serialize_schedules') as mock_serialize_schedules:
                mock_get_schedules.return_value = asyncio.Future()
                mock_get_schedules.return_value.set_result([sample_data])

                mock_serializer_instance = MagicMock()
                mock_serializer_instance.adata = asyncio.Future()
                mock_serializer_instance.adata.set_result([{
                    'course': sample_data.course.name,
                    'subject': sample_data.subject.name,
                    'teacher': sample_data.teacher.name,
                    'day_of_week': sample_data.day_of_week,
                    'start_time': sample_data.start_time.strftime("%H:%M"),
                }])

                mock_serialize_schedules.return_value = mock_serializer_instance

                response = await view(request)

                assert response.status_code == status.HTTP_200_OK
                assert response.data == [{
                    'course': sample_data.course.name,
                    'subject': sample_data.subject.name,
                    'teacher': sample_data.teacher.name,
                    'day_of_week': sample_data.day_of_week,
                    'start_time': sample_data.start_time.strftime("%H:%M"),
                }]

    async def test_get_class_schedules_not_cached(self, request_factory, view, schedule_factory):
        sample_data = await sync_to_async(schedule_factory.create)(course__name='TEST_COURSE')
        request = request_factory.get('/api/schedule/', {'class_name': sample_data.course.name})

        cache_key = f'schedules_False_{sample_data.course.name}'
        cache.delete(cache_key)

        with patch('apps.course.api.views.ScheduleAPIView.get_schedules') as mock_get_schedules:
            with patch('apps.course.api.views.ScheduleAPIView.serialize_schedules') as mock_serialize_schedules:
                mock_get_schedules.return_value = asyncio.Future()
                mock_get_schedules.return_value.set_result([sample_data])

                mock_serializer_instance = MagicMock()
                mock_serializer_instance.adata = asyncio.Future()
                mock_serializer_instance.adata.set_result([{
                    'course': sample_data.course.name,
                    'subject': sample_data.subject.name,
                    'teacher': sample_data.teacher.name,
                    'day_of_week': sample_data.day_of_week,
                    'start_time': sample_data.start_time.strftime("%H:%M"),
                }])

                mock_serialize_schedules.return_value = mock_serializer_instance

                response = await view(request)

                assert response.status_code == status.HTTP_200_OK
                assert response.data == [{
                    'course': sample_data.course.name,
                    'subject': sample_data.subject.name,
                    'teacher': sample_data.teacher.name,
                    'day_of_week': sample_data.day_of_week,
                    'start_time': sample_data.start_time.strftime("%H:%M"),
                }]


@pytest.mark.django_db
class TestCourseSerializer:
    def test_course_serializer(self):
        course = CourseFactory.create(name="Math 101")

        StudentFactory.create(name="John Doe", course=course)
        StudentFactory.create(name="Jane Doe", course=course)

        serializer = CourseSerializer(course)
        data = serializer.data

        assert data['name'] == "Math 101"
        assert data['student_count'] == 2


@pytest.mark.django_db
class TestScheduleSerializer:
    def test_schedule_serializer_with_factory(self):
        schedule = ScheduleFactory.create()
        serializer = ScheduleSerializer(schedule)
        data = serializer.data

        assert data['course']['name'] == schedule.course.name
        assert data['subject']['name'] == schedule.subject.name
        assert data['teacher']['name'] == schedule.teacher.name
        assert data['hour'] == schedule.start_time
