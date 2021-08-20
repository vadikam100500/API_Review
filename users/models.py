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
        default='user', verbose_name='Роль',
    )
    email = models.EmailField(max_length=60, blank=False, unique=True)
    bio = models.TextField(max_length=250, blank=True)

    class Meta:
        ordering = ('-pk',)
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='user_is_not_me'
            )
        ]

    def save(self, *args, **kwargs):
        if self.role == 'moderator':
            self.is_staff = True
        if self.role == 'admin':
            self.is_superuser = True
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
