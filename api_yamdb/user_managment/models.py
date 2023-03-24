from django.contrib.auth.models import AbstractUser
from django.db import models

# https://practicum.yandex.ru/learn/python-developer-plus/courses/9527ae09-177e-42cc-95fa-cd6a94de2352/sprints/100933/topics/5ea1635f-38e3-46e4-a2f7-cf66e430833d/lessons/e5c1629c-6bf5-40c7-a07d-1a8797ffc163/
# https://docs.djangoproject.com/en/4.1/ref/models/fields/
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLE_CHOICES = (
    (USER, 'пользователь'),
    (MODERATOR, 'модератор'),
    (ADMIN, 'администратор')
)


# https://code.s3.yandex.net/backend-developer/learning-materials/custom_User_model.pdf
# https://docs.djangoproject.com/en/3.2/ref/contrib/auth/#django.contrib.auth.models.User
class User(AbstractUser):
    """Модель пользователей."""
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    # переопределяем, т.к. в стандартной модели поле email - optional
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='E-mail пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        null=True,
        blank=True
    )
    # "user" "moderator" "admin"
    # Администратор, модератор или пользователь
    # По умолчанию user
    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль пользователя'
    )

    def __str__(self):
        return self.username
