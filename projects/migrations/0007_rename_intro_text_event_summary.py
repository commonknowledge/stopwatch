# Generated by Django 3.2.6 on 2021-08-24 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20210819_1736'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='intro_text',
            new_name='summary',
        ),
    ]