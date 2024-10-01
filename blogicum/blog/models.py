"""Модуль моделей прложения Blog.

Включает в себя модели:
Категория(Category)
Местоположение(Location)
Публикация(Pocn)
Автор(User)
"""
from django.db import models
from django.contrib.auth import get_user_model
from blogicum.models import BaseBlogModel
# Константа длины выводимого заголовка
LEN_TITLE = 50


User = get_user_model()  # Модель пользователя


class Category(BaseBlogModel):
    """Модель категорий"""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены '
                   'символы латиницы, цифры, дефис и подчёркивание.'
                   ))

    class Meta:

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class Location(BaseBlogModel):
    """Модель местоположений"""

    name = models.CharField(
        max_length=256,
        verbose_name='Название места',
    )

    class Meta:

        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name


class Post(BaseBlogModel):
    """модель публикаций"""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем '
                   '— можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        if len(self.title) > LEN_TITLE:
            return self.title[:LEN_TITLE] + '...'
        return self.title
