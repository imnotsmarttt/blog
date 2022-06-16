from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('blog/create/', views.CreateBlog.as_view(), name='blog_create'),
    path('blog/feed/', views.BlogFeed.as_view(), name='blog_feed'),
    path('blog/feed/rubric/<int:rubric>', views.BlogFeedByRubric.as_view(), name='blog_feed_by_rubric'),
    path('blog/<int:pk>/', views.BlogDetail.as_view(), name='blog_detail'),

    path('blog/<int:pk>/post/create/', views.CreatePost.as_view(), name='post_create'),
]
