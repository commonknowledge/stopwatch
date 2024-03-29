# Generated by Django 3.2.23 on 2023-11-08 15:13

from django.db import migrations, models
import wagtail.contrib.forms.models


class Migration(migrations.Migration):

    dependencies = [
        ('stopwatch', '0041_customcontentpage_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='from_address',
            field=models.EmailField(blank=True, max_length=255, verbose_name='from address'),
        ),
        migrations.AlterField(
            model_name='form',
            name='to_address',
            field=models.CharField(blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, validators=[wagtail.contrib.forms.models.validate_to_address], verbose_name='to address'),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='choices',
            field=models.TextField(blank=True, help_text='Comma or new line separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices'),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='default_value',
            field=models.TextField(blank=True, help_text='Default value. Comma or new line separated values supported for checkboxes.', verbose_name='default value'),
        ),
        migrations.AlterField(
            model_name='stopwatchimage',
            name='file_hash',
            field=models.CharField(blank=True, db_index=True, editable=False, max_length=40),
        ),
    ]
