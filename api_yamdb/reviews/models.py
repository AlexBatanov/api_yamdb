from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


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
    # переопределяем, т.к. в стандартной модели поле email - optional
    email = models.EmailField(
        max_length=254,
        verbose_name='E-mail пользователя')
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

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__exact='me'),
                name="username shouldn't be 'me'"
            )
        ]



class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Категория произведения'
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Slug категории произведения',
        unique=True
    )


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр произведения'
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Slug жанра произведения',
        unique=True
    )


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    # Нужна будет проверка, чтобы не было в будущем
    year = models.IntegerField(
        verbose_name='Год создания произведения',
        validators=[MaxValueValidator(timezone.now().year)]
    )
    # Поле будет расчетное
    rating = models.IntegerField(
        verbose_name='Рейтинг произведения',
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Ссылки на жанры произведения',
        through='TitleGenre'
    )
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/
    # При удалении объекта категории Category не нужно
    # удалять связанные с этой категорией произведения
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Ссылка на категорию произведения',
        null=True
    )


class TitleGenre(models.Model):
    """Модель связи произведений и жанров."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на жанр произведения'
    )


class Review(models.Model):
    """Модель отзывов на произведения."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на произведение',
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на автора отзыва',
        related_name='reviews'
    )
    # нужно ограничение от 1 до 10
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка отзыва',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время создания отзыва',
        auto_now_add=True
    )


class Comment(models.Model):
    """Модель комментариев на отзывы."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на отзыв',
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на автора комментария',
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время создания коммента',
        auto_now_add=True
    )
