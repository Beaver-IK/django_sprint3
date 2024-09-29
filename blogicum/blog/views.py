from django.shortcuts import render
from django.http import Http404, HttpRequest, HttpResponse
from blog.models import Post, Category
from django.utils import timezone
from django.db.models import Q, QuerySet, Model
from django.shortcuts import get_object_or_404
# Константа фильтров
FILTERS: dict = {
    'is_published': True,
    'pub_date__lte': timezone.now(),
    'category__is_published': True}


def filter_with_q(model: Model,
                  param: dict,
                  connect=None) -> QuerySet[Post]:
    """Функция фильтрации постов"""
    q: Q = Q(**param)
    if connect:
        return model.objects.select_related(*connect).filter(q)
    else:
        return model.objects.filter(q)


def index(request: HttpRequest) -> HttpResponse:
    """Функция главной страницы."""
    template: str = 'blog/index.html'
    connect: tuple = ('category',)
    post_list: QuerySet[Post] = filter_with_q(Post,
                                              FILTERS,
                                              connect=connect)[:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Функция полного просмотра поста."""
    template: str = 'blog/detail.html'
    connect: tuple = ('category', 'location', 'author',)
    post: Model.object[Post] = get_object_or_404(
        filter_with_q(Post, FILTERS, connect=connect), id=id
    )
    context: dict[str, dict] = {'post': post}
    return render(request, template, context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Функция фильтрации постов по категории."""
    template: str = 'blog/category.html'
    category: Model.object[Category] = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
            is_published=True))
    connect: tuple = ('category', 'location', 'author',)
    post_list: QuerySet[Post] = filter_with_q(
        Post,
        FILTERS,
        connect=connect).filter(
        category=category)
    if not category.is_published:
        raise Http404('Категория не найдена')
    context: dict = {
        'category': category,
        'post_list': post_list}
    return render(request, template, context)
