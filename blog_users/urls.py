from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='register'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('login/', views.UserLogin.as_view(), name='login'),
]