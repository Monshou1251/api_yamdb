from django.contrib.auth import get_user_model
from django.db import models

from users.models import User

from .validators import validate_year


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        verbose_name='Название произведения',
        max_length=256,
        db_index=True,
    )
    year = models.IntegerField(
        verbose_name='Год написания',
        validators=(validate_year,),
    )
    description = models.TextField(
        verbose_name='Краткое описание',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        db_index=True,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор ревью'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Запись, к которой относится ревью'
    )
    score = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        blank=False,
        null=False
    )
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['created']
        constraints = (models.UniqueConstraint(  # Тут сомнения, нужно обсудить
            fields=('title', 'author'),
            name='unique_review',
        ),)

    def __str__(self):
        return self.title


class Comments(models.Model):
    author = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Автор ревью'
    )
    post = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Запись, к которой относится ревью'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
