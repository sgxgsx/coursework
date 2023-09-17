from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class MyUserManager(UserManager):
    pass


class MyUser(AbstractUser):
    name = models.TextField(max_length=50, blank=False, null=False)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(null=False, blank=False)
    status = models.TextField(max_length=20, null=False, default="Agent")






