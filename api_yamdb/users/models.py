from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    ]
    role = models.CharField(
        max_length=40, choices=ROLE,
        default=ROLE, verbose_name='Роль')
    bio = models.TextField(max_length=250, blank=True)
    confirm_code = models.CharField(max_length=5)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_admin

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_moderator

    def __str__(self):
        return self.username
