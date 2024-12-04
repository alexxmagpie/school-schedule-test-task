import factory

from faker import Faker

from apps.core.factories import UserFactory
from apps.course.factories import CourseFactory

from apps.student import models


fake = Faker()


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Student

    name = factory.LazyAttribute(lambda x: fake.name())
    course = factory.SubFactory(CourseFactory)
    user = factory.SubFactory(UserFactory)
