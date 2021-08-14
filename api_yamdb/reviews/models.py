from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя категории')
    slug = models.SlugField(
        max_length=50, unique=True, null=True, verbose_name='Slug категории'
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя жанра')
    slug = models.SlugField(
        unique=True, max_length=50,  null=True, verbose_name='Slug жанра'
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.IntegerField(
        validators=[
            MaxValueValidator(datetime.now().year),
            MinValueValidator(1)
        ],
        null=True,
        verbose_name='Год создания произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='Жанр'
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name='Описание')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:50]


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="reviews", verbose_name='Произведениe'
    )
    text = models.TextField(verbose_name='Отзыв')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'],
                name='unique_name_reviews'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Коментируемый отзыв'
    )
    text = models.TextField(verbose_name='Коментарий')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, blank=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
