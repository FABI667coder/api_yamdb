from django.db import models


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
        return f'{self.name} {self.name}'


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
        return f'{self.name} {self.name}'


class Title(models.Model):
    name = models.CharField('Наименование', max_length=100)
    year = models.IntegerField()
    description = models.TextField(
        'Описание',
        max_length=300,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
        verbose_name='Жанр',
        verbose_name_plural = 'Жанры'
    )
    category = models.ForeignKey(
        Category,
        related_name='categories',
        verbose_name='Категория',
        verbose_name_plural = 'Категории'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
