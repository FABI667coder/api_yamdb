from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UsernameValidator

ROLES = (
    ('admin', 'admin'),
    ('moderator', 'moderator'),
    ('user', 'user'),
)


class User(AbstractUser):
    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        validators=[UsernameValidator],
    )
    email = models.EmailField(
        'Email',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default='user'
    )

    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True
    )

    def __str__(self):
        return str(self.username)

    def is_admin(self):
        return self.role == 'admin'

    def is_moderator(self):
        return self.role == 'moderator'

    def is_user(self):
        return self.role == 'user'
