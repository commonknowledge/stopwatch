# Generated by Django 3.2.23 on 2024-06-12 18:05

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stopwatch', '0045_auto_20240611_1331_squashed_0050_auto_20240611_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='pinned_pages',
            field=wagtail.fields.StreamField([('pinned_page', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock(help_text='Select a page to display at the top the category page.', required=False))]))], blank=True, use_json_field=None),
        ),
        migrations.DeleteModel(
            name='MultiPageSnippet',
        ),
    ]