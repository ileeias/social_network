# Generated by Django 5.1.3 on 2024-12-05 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_alter_comments_update_date_alter_posts_update_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='dislikes_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='posts',
            name='likes_count',
            field=models.IntegerField(default=0),
        ),
    ]
