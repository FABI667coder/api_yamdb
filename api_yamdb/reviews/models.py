from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import UsernameValidator, validate_year

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLES_CHOICES = [
    (ADMIN, 'admin'),
    (MODERATOR, 'moderator'),
    (USER, 'user'),
]


class User(AbstractUser):
    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        validators=[UsernameValidator()],
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
        choices=ROLES_CHOICES,
        default=USER
    )

    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        blank=True,
        null=True
    )

    @property
    def is_admin(self):
        return (self.role == ADMIN
                or self.is_staff
                or self.is_superuser
                )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=50)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Наименование', max_length=256)
    year = models.PositiveSmallIntegerField(
        validators=[validate_year]
    )
    description = models.TextField(
        'Описание',
        max_length=300,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        related_name='categories',
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    score = models.PositiveIntegerField(
        validators=(
            MinValueValidator(settings.MIN_SCORE),
            MaxValueValidator(settings.MAX_SCORE),
        ),
        verbose_name='Оценка произведения',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария',
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text[:settings.LENGTH_TEXT]
