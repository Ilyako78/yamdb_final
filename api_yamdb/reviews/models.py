from django.db import models
from django.db.models import SlugField, CharField
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from .validators import SLUG_VALIDATOR, year_validator


class BasicUserContent(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(
        verbose_name='Категория',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Адрес категории',
        max_length=50,
        unique=True,
        validators=[SLUG_VALIDATOR],
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> SlugField:
        return self.name


class GenreCategory(models.Model):
    name = models.CharField(max_length=50,)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        abstract = True


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(
        verbose_name='Жанр',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Адрес жанра',
        max_length=50,
        unique=True,
        validators=[SLUG_VALIDATOR],
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> CharField:
        return self.name


class Title(models.Model):
    """Произведение."""
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=(year_validator,),
        db_index=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Произведения-Жанры."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} - {self.title}'


class Review(BasicUserContent):
    """Отзывы."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('author', 'title',)


class Comment(BasicUserContent):
    """Комментарии."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['id', ]
