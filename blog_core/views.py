from django.shortcuts import render
from django.views.generic import CreateView, DetailView


from .forms import CreateBlogForm
from .models import Blog, BlogPost


def index(request):
    return render(request, 'base.html')


class CreateBlog(CreateView):
    """Представление создания блога"""
    form_class = CreateBlogForm
    template_name = 'core/create_blog.html'

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.is_active = True
        blog.creator = self.request.user
        blog.save()
        return super().form_valid(form)


    def get_success_url(self):
        return f'/user/profile/{self.request.user.id}/blogs/'


class BlogDetail(DetailView):
    """Детальное представление конкретного блога"""
    model = Blog
    template_name = 'core/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = BlogPost.objects.filter(blog=self.get_object())
        return context


class CreatePost(CreateView):
    """Представление публикации поста"""


class PostDetail(DetailView):
    """Детальное представление конкретнго поста"""
