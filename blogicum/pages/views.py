from django.shortcuts import render
from django.views.generic import TemplateView
from http import HTTPStatus


class About(TemplateView):
    template_name = 'pages/about.html'


class Rules(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=HTTPStatus.OK)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=HTTPStatus.OK)


def server_error(request):
    return render(request, 'pages/500.html', status=HTTPStatus.OK)
