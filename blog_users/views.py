from django.shortcuts import redirect, reverse
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator

from .forms import UserRegisterForm, UserAuthForm, UserEditProfileForm
from .models import CustomUser
from blog_core.models import Blog, BlogRubric


class UserRegister(CreateView):
    """Представление регистрации пользователя"""
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect('profile', pk=self.request.user.id)


class UserLogin(LoginView):
    """Представление входа пользователя"""
    template_name = 'users/login.html'
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
        return reverse('profile', kwargs={'pk': self.request.user.id})


class UserBlogs(DetailView):
    """Блоги конкретного пользователя"""
    template_name = 'users/user_blog.html'
    model = CustomUser
    context_object_name = 'user'
    paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_queryset = Blog.objects.filter(creator=self.get_object()).order_by('-created')
        blog_pagination = self.blog_paginator(queryset=blog_queryset)

        blog_count_check = blog_queryset.values('creator').count() > 3
        context['blog_count_check'] = blog_count_check
        context['blog_count'] = blog_queryset.values('creator').count()
        context['blogs'] = blog_pagination
        context['blog_rubric'] = BlogRubric.objects.all()
        return context

    def blog_paginator(self, queryset):
        paginator = Paginator(queryset, 2)
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities


class UserBlogsByRubric(DetailView):
    """Отсортированные блоги конкретного пользователя"""
    template_name = 'users/user_blog.html'
    model = CustomUser
    context_object_name = 'user'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_queryset = Blog.objects.filter(creator=self.get_object(),
                                               rubric=self.kwargs['rubric']).order_by('-created')
        blog_pagination = self.blog_paginator(queryset=blog_queryset)
        blog_count = blog_queryset
        context['blog_count'] = blog_count.values('creator').count()
        context['blogs'] = blog_pagination
        context['blog_rubric'] = BlogRubric.objects.all()
        return context

    def blog_paginator(self, queryset):
        paginator = Paginator(queryset, 2)
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities
