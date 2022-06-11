from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('blog/create/', views.CreateBlog.as_view(), name='blog_create'),
    path('blog/<int:pk>/', views.BlogDetail.as_view(), name='blog_detail')
]
