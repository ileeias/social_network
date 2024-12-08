# Generated by Django 5.1.3 on 2024-11-24 08:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_remove_posts_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.comments'),
        ),
    ]