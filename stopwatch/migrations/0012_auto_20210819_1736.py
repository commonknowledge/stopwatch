# Generated by Django 3.2.6 on 2021-08-19 17:36

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import stopwatch.models.core
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('stopwatch', '0011_sitesettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock()), ('quote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock())])), ('embed', wagtail.core.blocks.StructBlock([('embed_url', wagtail.core.blocks.URLBlock()), ('fullscreen', wagtail.core.blocks.BooleanBlock(default=False))])), ('downloads', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=False)), ('documents', wagtail.core.blocks.ListBlock(wagtail.documents.blocks.DocumentChooserBlock()))])), ('cta', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock(required=False)), ('target', wagtail.core.blocks.PageChooserBlock(required=True))])), ('links', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('message', wagtail.core.blocks.RichTextBlock(required=False)), ('links', wagtail.core.blocks.StreamBlock([('alert', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('content', wagtail.core.blocks.TextBlock())])), ('website', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.TextBlock(required=False)), ('url', wagtail.core.blocks.URLBlock())])), ('email', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.TextBlock(required=False)), ('address', wagtail.core.blocks.EmailBlock())])), ('page', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.TextBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock())]))]))])), ('newsletter_signup', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock(required=False)), ('target', wagtail.core.blocks.PageChooserBlock(required=True))])), ('person_listing', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('people', wagtail.core.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(stopwatch.models.core.Person)))])), ('alert', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('content', wagtail.core.blocks.TextBlock())]))], blank=True),
        ),
        migrations.AlterField(
            model_name='form',
            name='thank_you_page',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock()), ('quote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock())])), ('embed', wagtail.core.blocks.StructBlock([('embed_url', wagtail.core.blocks.URLBlock()), ('fullscreen', wagtail.core.blocks.BooleanBlock(default=False))])), ('downloads', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=False)), ('documents', wagtail.core.blocks.ListBlock(wagtail.documents.blocks.DocumentChooserBlock()))])), ('cta', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock(required=False)), ('target', wagtail.core.blocks.PageChooserBlock(required=True))])), ('links', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('message', wagtail.core.blocks.RichTextBlock(required=False)), ('links', wagtail.core.blocks.StreamBlock([('alert', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('content', wagtail.core.blocks.TextBlock())])), ('website', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.TextBlock(required=False)), ('url', wagtail.core.blocks.URLBlock())])), ('email', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.TextBlock(required=False)), ('address', wagtail.core.blocks.EmailBlock())])), ('page', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.TextBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock())]))]))])), ('newsletter_signup', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock(required=False)), ('target', wagtail.core.blocks.PageChooserBlock(required=True))])), ('person_listing', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('people', wagtail.core.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(stopwatch.models.core.Person)))])), ('alert', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('content', wagtail.core.blocks.TextBlock())]))]),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='body',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock()), ('quote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock())])), ('embed', wagtail.core.blocks.StructBlock([('embed_url', wagtail.core.blocks.URLBlock()), ('fullscreen', wagtail.core.blocks.BooleanBlock(default=False))])), ('downloads', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=False)), ('documents', wagtail.core.blocks.ListBlock(wagtail.documents.blocks.DocumentChooserBlock()))])), ('cta', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock(required=False)), ('target', wagtail.core.blocks.PageChooserBlock(required=True))])), ('links', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('message', wagtail.core.blocks.RichTextBlock(required=False)), ('links', wagtail.core.blocks.StreamBlock([('alert', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('content', wagtail.core.blocks.TextBlock())])), ('website', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.TextBlock(required=False)), ('url', wagtail.core.blocks.URLBlock())])), ('email', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.TextBlock(required=False)), ('address', wagtail.core.blocks.EmailBlock())])), ('page', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.TextBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock())]))]))])), ('newsletter_signup', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock(required=False)), ('target', wagtail.core.blocks.PageChooserBlock(required=True))])), ('person_listing', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('people', wagtail.core.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(stopwatch.models.core.Person)))])), ('alert', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('content', wagtail.core.blocks.TextBlock())])), ('articles_list', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('site_area', wagtail.core.blocks.PageChooserBlock(page_type=['stopwatch.Category']))])), ('tabs', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock()), ('tabs', wagtail.core.blocks.StreamBlock([('stats', wagtail.core.blocks.StructBlock([('icon', wagtail.core.blocks.ChoiceBlock(choices=[('chat-left', 'Speech Bubble'), ('grap-up', 'Graph'), ('hammer', 'Gavel')], template='widgets/icon_block.html')), ('short_title', wagtail.core.blocks.CharBlock()), ('title', wagtail.core.blocks.CharBlock()), ('call_to_action', wagtail.core.blocks.CharBlock(required=False)), ('related_page', wagtail.core.blocks.PageChooserBlock(required=False))])), ('info', wagtail.core.blocks.StructBlock([('icon', wagtail.core.blocks.ChoiceBlock(choices=[('chat-left', 'Speech Bubble'), ('grap-up', 'Graph'), ('hammer', 'Gavel')], template='widgets/icon_block.html')), ('short_title', wagtail.core.blocks.CharBlock()), ('title', wagtail.core.blocks.CharBlock()), ('call_to_action', wagtail.core.blocks.CharBlock(required=False)), ('related_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('content', wagtail.core.blocks.RichTextBlock()), ('author', wagtail.snippets.blocks.SnippetChooserBlock('stopwatch.Person', required=False))]))]))]))], blank=True),
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='stopwatch.article')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stopwatch_articletag_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='stopwatch.ArticleTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
