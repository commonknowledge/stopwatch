# Generated by Django 3.2.23 on 2024-08-21 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stopwatch', '0051_alter_categorychildpage_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorychildpagesection',
            name='title',
            field=models.CharField(blank=True, help_text='Title for this section of child pages', max_length=255, null=True),
        ),
    ]
