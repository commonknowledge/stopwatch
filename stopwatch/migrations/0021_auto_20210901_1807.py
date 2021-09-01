# Generated by Django 3.2.6 on 2021-09-01 18:07

from django.db import migrations, models
import stopwatch.models.core
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('stopwatch', '0020_auto_20210826_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='style',
            field=models.CharField(choices=[('GRID', 'Grid'), ('ROWS', 'Rows')], default='GRID', max_length=128),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='body',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock()), ('quote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock())])), ('embed', wagtail.core.blocks.StructBlock([('embed_url', wagtail.core.blocks.URLBlock()), ('fullscreen', wagtail.core.blocks.BooleanBlock(default=False))])), ('downloads', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=False)), ('documents', wagtail.core.blocks.ListBlock(wagtail.documents.blocks.DocumentChooserBlock()))])), ('cta', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock(required=False)), ('target', wagtail.core.blocks.PageChooserBlock(required=True))])), ('links', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('message', wagtail.core.blocks.RichTextBlock(required=False)), ('links', wagtail.core.blocks.StreamBlock([('alert', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('content', wagtail.core.blocks.TextBlock())])), ('website', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.TextBlock(required=False)), ('url', wagtail.core.blocks.URLBlock())])), ('email', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.TextBlock(required=False)), ('address', wagtail.core.blocks.EmailBlock())])), ('page', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.TextBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock())]))]))])), ('newsletter_signup', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock(required=False)), ('target', wagtail.core.blocks.PageChooserBlock(required=True))])), ('person_listing', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('people', wagtail.core.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(stopwatch.models.core.Person)))])), ('alert', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('content', wagtail.core.blocks.TextBlock())])), ('articles_list', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('site_area', wagtail.core.blocks.PageChooserBlock(page_type=['stopwatch.Category'])), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('GRID', 'Grid'), ('ROWS', 'Rows')]))]))], blank=True),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='page_description',
            field=models.CharField(default='Research and action for fair and accountable policing', max_length=128),
        ),
    ]
