# Generated by Django 5.1.3 on 2024-11-24 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_posts_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='comment',
        ),
    ]
