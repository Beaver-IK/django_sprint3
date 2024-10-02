from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from blog.models import Post, Category
from django.utils.timezone import now
from django.db.models import QuerySet, Model
from django.shortcuts import get_object_or_404
from typing import Union


def index(request: HttpRequest) -> HttpResponse:
    """Функция главной страницы."""
    template: str = 'blog/index.html'
    post_list: QuerySet[Post] = Post.objects.filter(
        is_published=True,
        pub_date__lte=now(),
        category__is_published=True)[:5]
    context: dict[str, QuerySet[Post]] = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Функция полного просмотра поста."""
    template: str = 'blog/detail.html'
    post: Post = get_object_or_404(Post.objects.filter(
        is_published=True,
        pub_date__lte=now(),
        category__is_published=True), id=id)
    context: dict[str, Post] = {'post': post}
    return render(request, template, context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Функция фильтрации постов по категории."""
    template: str = 'blog/category.html'
    category: Category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
            is_published=True))
    post_list: QuerySet[Post] = category.posts.filter(
        is_published=True,
        pub_date__lte=now(),
        category__is_published=True)
    context: dict[str, Union[Model, QuerySet[Post]]] = {
        'category': category,
        'post_list': post_list}

    return render(request, template, context)
