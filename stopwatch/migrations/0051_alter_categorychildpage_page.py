# Generated by Django 3.2.23 on 2024-08-21 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stopwatch', '0050_alter_category_display_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorychildpage',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='stopwatch.article'),
        ),
    ]
