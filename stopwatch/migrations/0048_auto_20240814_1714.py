# Generated by Django 3.2.23 on 2024-08-14 17:14

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stopwatch', '0047_categorychildpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorychildpage',
            name='category',
        ),
        migrations.CreateModel(
            name='CategoryChildPageSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('title', models.CharField(help_text='Title for this section of child pages', max_length=255)),
                ('category', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_page_sections', to='stopwatch.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='categorychildpage',
            name='section',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordered_child_pages', to='stopwatch.categorychildpagesection'),
        ),
    ]