# Generated by Django 3.2.6 on 2021-08-23 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stopwatch', '0014_auto_20210823_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='style',
        ),
        migrations.RemoveField(
            model_name='landingpage',
            name='page_description',
        ),
        migrations.AddField(
            model_name='category',
            name='navigable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='landingpage',
            name='newsflash_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stopwatch.category'),
        ),
    ]