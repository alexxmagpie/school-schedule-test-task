from rest_framework import serializers

from apps.core.api.serializers import ADRFModelSerializer

from apps.course import models

from apps.teacher.api.serializers import SubjectSerializer
from apps.teacher.api.serializers import TeacherSerializer


class CourseSerializer(ADRFModelSerializer):
    student_count = serializers.IntegerField(source='students.count', read_only=True)

    class Meta:
        model = models.Course
        fields = ['name', 'student_count']


class ScheduleSerializer(ADRFModelSerializer):
    course = CourseSerializer()
    subject = SubjectSerializer()
    teacher = TeacherSerializer()
    hour = serializers.SerializerMethodField()

    class Meta:
        model = models.Schedule
        fields = [
            'course',
            'subject',
            'teacher',
            'day_of_week',
            'hour'
        ]

    def get_hour(self, obj):
        return obj.start_time
