from django.shortcuts import render, reverse
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect

from .forms import CreateBlogForm, CreatePostForm, CommentForm
from .models import Blog, BlogPost, PostLike, Comment

from .services import is_fan, BlogFeedMixin

def index(request):
    return render(request, 'base.html')


class CreateBlog(LoginRequiredMixin, CreateView):
    """Представление создания блога"""
    form_class = CreateBlogForm
    template_name = 'core/create_blog.html'
    login_url = 'login'

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
            blog.editors.add(self.request.user.id)
            return super().form_valid(form)

    def get_success_url(self):
        return f'/user/profile/{self.request.user.id}/blogs/'


class BlogFeed(BlogFeedMixin, ListView):
    """Страница всех блогов"""
    model = Blog
    template_name = 'core/blog_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_blog_context(blog_pag=BlogFeedMixin.blog_paginator(self,
                                                                            request=self.request, queryset=Blog.objects.all()))
        context.update(c_def)
        return context


class BlogFeedByRubric(BlogFeedMixin, ListView):
    """Страница всех блогов по рубрикам"""
    model = Blog
    template_name = 'core/blog_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_blog_context(blog_pag=BlogFeedMixin.blog_paginator(self,
                                                                            request=self.request,
                                                                            queryset=Blog.objects.filter(rubric=self.kwargs['rubric'])))
        context.update(c_def)
        return context


class BlogDetail(DetailView):
    """Детальное представление конкретного блога"""
    model = Blog
    template_name = 'core/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = BlogPost.objects.filter(blog=self.get_object()).order_by('-created')
        return context


class BlogEditors(DetailView):
    model = Blog
    template_name = 'core/blog_editors.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['posts'] = BlogPost.objects.filter(blog=self.get_object()).order_by('-created')
    #     return context


class CreatePost(LoginRequiredMixin, CreateView):
    """Представление публикации поста"""
    form_class = CreatePostForm
    template_name = 'core/post_create.html'
    login_url = 'login'

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


class PostDetail(DetailView, FormMixin):
    """Детальное представление конкретнго поста"""
    model = BlogPost
    template_name = 'core/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = Blog.objects.get(id=self.kwargs['blog_id'])
        context['post_likes'] = PostLike.objects.filter(post=self.get_object())
        context['comments'] = Comment.objects.filter(post=self.kwargs['pk']).order_by('-created')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        if self.request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.user = self.request.user
            comment.post = self.get_object()
            comment.save()
            return super(PostDetail, self).form_valid(form)
        else:
            form.add_error('__all__', 'Комментарий могут оставлять только аутентифицированные пользователи))')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'blog_id': self.kwargs['blog_id'], 'pk': self.kwargs['pk']})


def post_like(request, post_id):
    # Лайк поста
    post = BlogPost.objects.get(id=post_id)
    if request.user.is_authenticated:
        if not is_fan(user=request.user, obj=post):
            post_like = PostLike()
            post_like.user = (request.user)
            post_like.post = post
            post_like.save()
        return HttpResponseRedirect(reverse('post_detail', kwargs={'blog_id': post.blog.id, 'pk':post.id}))
    else:
        return HttpResponseRedirect(reverse('post_detail', kwargs={'blog_id': post.blog.id, 'pk':post.id}))
