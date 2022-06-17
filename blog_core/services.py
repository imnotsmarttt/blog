from django.core.paginator import Paginator
from django.views.generic.list import ListView

from .models import PostLike, Blog, BlogRubric


def is_fan(obj, user) -> bool:
    """Проверяет, лайкнул ли `user` `obj`.
    """
    if not user.is_authenticated:
        return False
    likes = PostLike.objects.filter(
        user=user, post=obj)
    return likes.exists()


class BlogFeedMixin:
    """Миксин контекста и пагинации страницы блогов"""
    def get_blog_context(self, blog_pag, **kwargs):
        context = kwargs
        blog_pagination = blog_pag
        context['blogs'] = blog_pagination
        context['blog_rubric'] = BlogRubric.objects.all()
        return context

    def blog_paginator(self, request, queryset):
        paginator = Paginator(queryset, 10)
        page = request.GET.get('page')
        activities = paginator.get_page(page)
        return activities