# Generated by Django 5.1.3 on 2024-12-03 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_remove_posts_comment_posts_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
