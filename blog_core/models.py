from django.db import models

from blog_users.models import CustomUser


class BlogRubric(models.Model):
    """Рубрики поста"""
    name = models.CharField(max_length=50, verbose_name='Имя рубрики', db_index=True)

    class Meta:
        db_table = 'BlogRubric'

    def __str__(self):
        return self.name


class Blog(models.Model):
    """Набор постов в конкретном блоге"""
    name = models.CharField(max_length=50, verbose_name='Название блога')
    description = models.TextField(verbose_name='Описание блога')
    rubric = models.ForeignKey('BlogRubric', on_delete=models.CASCADE, related_name='blog_rubric')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_creator')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField()

    class Meta:
        db_table = 'Blog'

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """Публикация в конкретном блоге"""
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    images = models.ImageField(upload_to='post_img/', blank=True, verbose_name='Изображение')
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='blog')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='post_author')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    is_active = models.BooleanField()

    class Meta:
        db_table = 'BlogPost'

    def __str__(self):
        return self.title


class PostLike(models.Model):
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='post')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='like')
