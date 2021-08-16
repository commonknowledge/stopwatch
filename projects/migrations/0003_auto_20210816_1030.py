# Generated by Django 3.2.6 on 2021-08-16 10:30

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stopwatch', '0009_auto_20210813_1712'),
        ('projects', '0002_auto_20210813_1712'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='speakers',
        ),
        migrations.CreateModel(
            name='EventSpeaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='speakers', to='projects.event')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='stopwatch.person')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
