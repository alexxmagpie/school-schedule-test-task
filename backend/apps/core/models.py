from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Use custom User model in case of any extensions.
    """
    pass
