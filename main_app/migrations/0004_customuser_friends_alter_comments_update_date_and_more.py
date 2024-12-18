# Generated by Django 5.1.3 on 2024-11-14 15:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_friends_posts_likes_dislikes_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='friends',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comments',
            name='update_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='update_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
