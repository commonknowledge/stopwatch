# Generated by Django 3.2.23 on 2024-08-20 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stopwatch', '0048_auto_20240814_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='pinned_pages',
        ),
        migrations.RemoveField(
            model_name='category',
            name='pinned_pages_style',
        ),
        migrations.AddField(
            model_name='category',
            name='display_mode',
            field=models.CharField(choices=[('articles', 'Published Articles'), ('sections', 'Child List Sections')], default='articles', max_length=20),
        ),
    ]
