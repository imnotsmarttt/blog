from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'last_login', 'date_joined', 'country', 'region']


admin.site.register(CustomUser, CustomUserAdmin)

