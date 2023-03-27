from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    email = models.CIEmailField(
        max_length=254, unique=True, blank=False)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Логин пользователя имеет некорректный формат!'
            ),
        )
    )
    first_name = models.CharField(
        max_length=150, blank=False
    )
    last_name = models.CharField(
        max_length=150, blank=False
    )
    password = models.CharField(
        max_length=150, blank=False
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            )
        ]
