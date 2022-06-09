from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='register'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('login/', views.UserLogin.as_view(), name='login'),

    path('profile/<int:pk>/', views.UserProfile.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', views.UserEditProfile.as_view(), name='profile_edit'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)