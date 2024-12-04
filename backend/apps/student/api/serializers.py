from rest_framework import serializers

from apps.student import models


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['name', 'course']
