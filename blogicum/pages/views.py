from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def about(request: HttpRequest) -> HttpResponse:
    """Функция описания проекта."""
    template: str = 'pages/about.html'
    return render(request, template)


def rules(request: HttpRequest) -> HttpResponse:
    """Функция свода правил проекта."""
    template: str = 'pages/rules.html'
    return render(request, template)
