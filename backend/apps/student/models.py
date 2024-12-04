from django.contrib.auth import get_user_model
from django.db import models

from apps.course.models import Course


User = get_user_model()


class Student(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, related_name='students', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Student: {self.pk}, {self.name}>"
