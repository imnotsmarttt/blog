# Generated by Django 3.0.2 on 2022-06-09 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_users', '0002_auto_20220608_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='user_avatar/blank-profile-picture.png', upload_to='user_avatar/', verbose_name='Аватарка'),
        ),
    ]
