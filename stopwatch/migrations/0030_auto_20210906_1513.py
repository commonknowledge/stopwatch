# Generated by Django 3.2.6 on 2021-09-06 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stopwatch', '0029_landingpage_search_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='search_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='stopwatch.stopwatchimage', verbose_name='Search image'),
        ),
        migrations.AddField(
            model_name='category',
            name='search_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='stopwatch.stopwatchimage', verbose_name='Search image'),
        ),
    ]
