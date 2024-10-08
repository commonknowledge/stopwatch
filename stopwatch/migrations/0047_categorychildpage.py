# Generated by Django 3.2.23 on 2024-08-14 16:53

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
        ('stopwatch', '0046_auto_20240612_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryChildPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('category', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_child_pages', to='stopwatch.category')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.page')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
