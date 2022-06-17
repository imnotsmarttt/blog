from django.shortcuts import render, reverse
from django.views.generic import CreateView, DetailView, ListView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from .forms import CreateBlogForm, CreatePostForm
from .models import Blog, BlogPost, BlogRubric, PostLike

from .services import is_fan, BlogFeedMixin

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


class BlogFeed(BlogFeedMixin, ListView):
    """Страница всех блогов"""
    model = Blog
    template_name = 'core/blog_list.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        blog_p = BlogFeedMixin.blog_paginator(self, request=self.request, queryset=Blog.objects.all())
        context = super().get_context_data(**kwargs)
        c_def = self.get_blog_context(blog_pag=blog_p)
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class BlogFeedByRubric(BlogFeedMixin, ListView):
    """Страница всех блогов по рубрикам"""
    model = Blog
    template_name = 'core/blog_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        blog_p = BlogFeedMixin.blog_paginator(self, request=self.request,
                                              queryset=Blog.objects.filter(rubric=self.kwargs['rubric']))
        context = super().get_context_data(**kwargs)
        c_def = self.get_blog_context(blog_pag=blog_p)
        context = dict(list(context.items()) + list(c_def.items()))
        return context


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
    model = BlogPost
    template_name = 'core/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = Blog.objects.get(id=self.kwargs['blog_id'])
        context['post_likes'] = PostLike.objects.filter(post=self.get_object())
        return context


def post_like(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    if not is_fan(user=request.user, obj=post):
        post_like = PostLike()
        post_like.user = (request.user)
        post_like.post = post
        post_like.save()
    return HttpResponseRedirect(reverse('post_detail', kwargs={'blog_id': post.blog.id, 'pk':post.id}))

