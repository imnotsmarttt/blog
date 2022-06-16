from django.shortcuts import render, reverse
from django.views.generic import CreateView, DetailView, ListView
from django.core.paginator import Paginator

from .forms import CreateBlogForm, CreatePostForm
from .models import Blog, BlogPost, BlogRubric


def index(request):
    return render(request, 'base.html')


class CreateBlog(CreateView):
    """Представление создания блога"""
    form_class = CreateBlogForm
    template_name = 'core/create_blog.html'

    def form_valid(self, form):
        blog_count_check = Blog.objects.filter(creator=self.request.user).values('creator').count() >= 3
        if blog_count_check:
            form.add_error('__all__', 'У вас максимальное кол-во записей')
            return self.form_invalid(form)
        else:
            blog = form.save(commit=False)
            blog.is_active = True
            blog.creator = self.request.user
            blog.save()
            return super().form_valid(form)

    def get_success_url(self):
        return f'/user/profile/{self.request.user.id}/blogs/'


class BlogFeed(ListView):
    """Страница всех блогов"""
    model = Blog
    template_name = 'core/blog_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_queryset = Blog.objects.all().order_by('-created')
        blog_pagination = self.blog_paginator(queryset=blog_queryset)

        context['blogs'] = blog_pagination
        context['blog_rubric'] = BlogRubric.objects.all()
        return context

    def blog_paginator(self, queryset):
        paginator = Paginator(queryset, 10)
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities


class BlogFeedByRubric(ListView):
    """Страница всех блогов по рубрикам"""
    model = Blog
    template_name = 'core/blog_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_queryset = Blog.objects.filter(rubric=self.kwargs['rubric']).order_by('-created')
        blog_pagination = self.blog_paginator(queryset=blog_queryset)
        context['blogs'] = blog_pagination
        context['blog_rubric'] = BlogRubric.objects.all()
        return context

    def blog_paginator(self, queryset):
        paginator = Paginator(queryset, 10)
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities


class BlogDetail(DetailView):
    """Детальное представление конкретного блога"""
    model = Blog
    template_name = 'core/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = BlogPost.objects.filter(blog=self.get_object()).order_by('-created')
        return context


class CreatePost(CreateView):
    """Представление публикации поста"""
    form_class = CreatePostForm
    template_name = 'core/post_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = Blog.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        f.blog = self.get_context_data()['blog']
        f.is_active = True
        f.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog_detail', kwargs={'pk': self.get_context_data()['blog'].id})


class PostDetail(DetailView):
    """Детальное представление конкретнго поста"""
