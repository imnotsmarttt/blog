from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate

from .forms import UserRegisterForm, UserAuthForm, UserEditProfileForm
from .models import CustomUser
from blog_core.models import Blog, BlogRubric


class UserRegister(CreateView):
    """Представление регистрации пользователя"""
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(self.request, user)
            return redirect('index')


class UserLogin(LoginView):
    """Представление входа пользователя"""
    template_name = 'users/login.html'
    success_url = 'index/'
    form_class = UserAuthForm


class UserLogout(LogoutView):
    """Представление выхода пользователя"""
    template_name = 'users/logout.html'


class UserProfile(DetailView):
    """Профиль пользователя"""
    model = CustomUser
    context_object_name = 'user'
    template_name = 'users/profile.html'


class UserEditProfile(UpdateView):
    """Редиктирование профиля пользователя"""
    form_class = UserEditProfileForm
    model = CustomUser
    template_name = 'users/edit_profile.html'

    def get_success_url(self):
        return f'/user/profile/{self.request.user.id}/'


# class UserBlogs(DetailView):
#     template_name = 'users/user_blog.html'
#     model = Blog
#
#     def get_queryset(self):
#         queryset = Blog.objects.filter(creator=self.request.user)
#         return queryset

def user_blogs(request, creator):
    """Блоги юзера"""
    user = CustomUser.objects.get(id=creator)
    blogs = Blog.objects.filter(creator=user, is_active=True)
    blog_rubric = BlogRubric.objects.all()
    context = {
        'blogs': blogs,
        'user': user,
        'blog_rubric': blog_rubric
    }
    return render(request, 'users/user_blog.html', context)


def user_blogs_by_rubric(request, creator, pk):
    user = CustomUser.objects.get(id=creator)
    blogs = Blog.objects.filter(creator=user, is_active=True, rubric=pk)
    blog_rubrics = BlogRubric.objects.all()
    context ={
            'blogs': blogs,
            'user': user,
            'blog_rubric': blog_rubrics
        }
    return render(request, 'users/user_blog.html', context)