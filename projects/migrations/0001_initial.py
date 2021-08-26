# Generated by Django 3.2.6 on 2021-08-13 16:16

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('stopwatch', '0008_auto_20210813_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventTheme',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', max_length=18)),
                ('description', models.TextField()),
                ('body', wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock()), ('embed', wagtail.core.blocks.StructBlock([('embed_url', wagtail.core.blocks.URLBlock())])), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('cta', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock()), ('target', wagtail.core.blocks.PageChooserBlock(required=False))])), ('newsletter_signup', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock()), ('target', wagtail.core.blocks.PageChooserBlock(required=False))]))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProjectEvents',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProjectArticle',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('description', wagtail.core.fields.RichTextField()),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stopwatch.stopwatchimage')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('description', wagtail.core.fields.RichTextField()),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', max_length=18)),
                ('body', wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock()), ('embed', wagtail.core.blocks.StructBlock([('embed_url', wagtail.core.blocks.URLBlock())])), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('cta', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock()), ('target', wagtail.core.blocks.PageChooserBlock(required=False))])), ('newsletter_signup', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock()), ('target', wagtail.core.blocks.PageChooserBlock(required=False))]))])),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stopwatch.stopwatchimage')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro_text', models.CharField(blank=True, default='', max_length=1024)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('body', wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock()), ('embed', wagtail.core.blocks.StructBlock([('embed_url', wagtail.core.blocks.URLBlock())])), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('cta', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock()), ('target', wagtail.core.blocks.PageChooserBlock(required=False))])), ('newsletter_signup', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock()), ('target', wagtail.core.blocks.PageChooserBlock(required=False))]))])),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stopwatch.stopwatchimage')),
                ('speakers', models.ManyToManyField(to='stopwatch.Person')),
                ('theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.eventtheme')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]