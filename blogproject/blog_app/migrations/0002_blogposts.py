# Generated by Django 4.1 on 2023-07-04 16:52

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_title', models.CharField(max_length=100)),
                ('blog_content', ckeditor.fields.RichTextField()),
                ('blog_image', models.CharField(max_length=100)),
                ('blog_created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('blog_published_date', models.DateTimeField(blank=True, null=True)),
                ('blog_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
