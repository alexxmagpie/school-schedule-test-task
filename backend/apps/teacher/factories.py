import factory

from faker import Faker

from apps.core.factories import UserFactory

from apps.teacher import models


fake = Faker()


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Teacher

    name = factory.LazyAttribute(lambda x: fake.user_name())
    user = factory.SubFactory(UserFactory)


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Subject

    name = factory.LazyAttribute(lambda x: fake.user_name())
    teacher = factory.SubFactory(TeacherFactory)
