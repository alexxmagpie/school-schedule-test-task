from django.db import models

from apps.teacher.models import Subject
from apps.teacher.models import Teacher


class Course(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Course: {self.pk}, {self.name}>"


class Schedule(models.Model):

    class DayOfWeekChoices(models.TextChoices):
        MONDAY = 'Monday', 'Monday'
        TUESDAY = 'Tuesday', 'Tuesday'
        WEDNESDAY = 'Wednesday', 'Wednesday'
        THURSDAY = 'Thursday', 'Thursday'
        FRIDAY = 'Friday', 'Friday'

    course = models.ForeignKey(Course, related_name='courses', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='schedules', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='schedules', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=9, choices=DayOfWeekChoices.choices, db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'subject', 'teacher', 'day_of_week', 'start_time', 'end_time'],
                name='unique_schedule'
            )
        ]

    def save(self, *args, **kwargs):
        # Make sure teacher does not already have a course at that time.
        if self.teacher.schedules.filter(day_of_week=self.day_of_week, start_time=self.start_time).exists():
            raise models.ValidationError('This teacher already has a course at provided day and time.')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.name} -> {self.subject.name} | {self.day_of_week}, {self.start_time}"

    def __repr__(self):
        return f"<Schedule: {self.pk}, {self.course.name} -> {self.subject.name}>"
