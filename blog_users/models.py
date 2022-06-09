from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Расширенная модель пользователя"""
    avatar = models.ImageField(upload_to='user_avatar/', verbose_name='Аватарка',
                               default='user_avatar/blank-profile-picture.png')
    country = models.CharField(max_length=50, verbose_name='Страна')
    region = models.CharField(max_length=50, verbose_name='Регион')
    about = models.TextField(blank=True, null=True, verbose_name='О себе')

    class Meta:
        db_table = 'CustomUser'
