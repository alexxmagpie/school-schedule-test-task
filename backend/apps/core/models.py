from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Use custom User model in case of any extensions.
    """
    pass
