from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('blog/create/', views.CreateBlog.as_view(), name='blog_create'),
]
