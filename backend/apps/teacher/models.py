from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Teacher: {self.pk}, {self.name}>"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, related_name='subjects', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Subject: {self.pk}, {self.name}>"
