from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]
    role = models.CharField(
        max_length=40, choices=ROLE,
        default=ROLE, verbose_name='Роль'
    )
    bio = models.TextField(max_length=250, blank=True)
    confirm_code = models.CharField(max_length=5)

    def save(self, *args, **kwargs):
        self.is_active = True
        if self.role == "moderator":
            self.is_staff = True
        if self.role == "admin":
            self.is_superuser = True
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
