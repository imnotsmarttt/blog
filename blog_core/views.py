from django.shortcuts import render
from django.views.generic import CreateView, DetailView


from .forms import CreateBlogForm


def index(request):
    return render(request, 'base.html')


class CreateBlog(CreateView):
    """Представление создания блога"""
    form_class = CreateBlogForm
    template_name = 'core/create_blog.html'


class BlogDetail(DetailView):
    """Детальное представление конкретного блога"""


class CreatePost(CreateView):
    """Представление публикации поста"""


class PostDetail(DetailView):
    """Детальное представление конкретнго поста"""
