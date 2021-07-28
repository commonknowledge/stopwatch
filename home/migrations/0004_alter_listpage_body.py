# Generated by Django 3.2.5 on 2021-07-27 18:40

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210727_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listpage',
            name='body',
            field=wagtail.core.fields.StreamField([('articles_list', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('site_area', wagtail.core.blocks.PageChooserBlock(page_type=['home.ListPage']))])), ('cta', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock()), ('target', wagtail.core.blocks.PageChooserBlock(required=False))])), ('newsletter_signup', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock()), ('target', wagtail.core.blocks.PageChooserBlock(required=False))]))], blank=True),
        ),
    ]
