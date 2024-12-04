import datetime
import random
import factory

from faker import Faker

from apps.course import models

from apps.teacher.factories import SubjectFactory
from apps.teacher.factories import TeacherFactory


fake = Faker()


def random_schedule_time():
    hour = random.randint(8, 16)
    return datetime.time(hour=hour, minute=0)


def random_course_name():
    return f'{random.randint(1,8)}{random.choice(["A", "B", "C", "D", "E"])}'


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Course

    name = factory.LazyFunction(random_course_name)


class ScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Schedule

    day_of_week = factory.LazyAttribute(lambda x: fake.day_of_week())
    start_time = factory.LazyFunction(random_schedule_time)
    end_time = factory.LazyAttribute(lambda obj: datetime.time(hour=obj.start_time.hour+1, minute=0))
    course = factory.SubFactory(CourseFactory)
    subject = factory.SubFactory(SubjectFactory)
    teacher = factory.SubFactory(TeacherFactory)
