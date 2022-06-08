from django.contrib import admin

from .models import BlogRubric, BlogPost, Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rubric', 'creator', 'created', 'is_active']


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'blog', 'author', 'created', 'updated', 'is_active']


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogRubric)
admin.site.register(BlogPost, BlogPostAdmin)