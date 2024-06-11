# Generated by Django 3.2.23 on 2024-06-11 15:19

from django.db import migrations, models
import modelcluster.fields
import stopwatch.models.core
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    replaces = [('stopwatch', '0045_auto_20240611_1331'), ('stopwatch', '0046_category_pinned_page'), ('stopwatch', '0047_category_pinned_page_style'), ('stopwatch', '0048_auto_20240611_1358'), ('stopwatch', '0049_auto_20240611_1416'), ('stopwatch', '0050_auto_20240611_1421')]

    dependencies = [
        ('stopwatch', '0044_alter_article_body_alter_articletag_tag_and_more'),
        ('wagtailcore', '0078_referenceindex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=wagtail.fields.StreamField([('text', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'])), ('embed', wagtail.blocks.StructBlock([('embed_url', wagtail.blocks.URLBlock()), ('fullscreen', wagtail.blocks.BooleanBlock(default=False, required=False))])), ('downloads', wagtail.blocks.StructBlock([('documents', wagtail.blocks.ListBlock(wagtail.documents.blocks.DocumentChooserBlock()))])), ('cta', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'], required=False)), ('target', wagtail.blocks.PageChooserBlock(required=True))])), ('form', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'], required=False)), ('target', wagtail.blocks.PageChooserBlock('stopwatch.Form', required=True))])), ('links', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('message', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'], required=False)), ('links', wagtail.blocks.StreamBlock([('alert', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock()), ('content', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link']))])), ('website', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock()), ('name', wagtail.blocks.CharBlock(required=False))])), ('email', wagtail.blocks.StructBlock([('address', wagtail.blocks.EmailBlock()), ('name', wagtail.blocks.CharBlock(required=False))])), ('page', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock()), ('name', wagtail.blocks.CharBlock(required=False))]))]))])), ('newsletter_signup', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'], required=False)), ('target', wagtail.blocks.PageChooserBlock(required=True))])), ('person_listing', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('people', wagtail.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(stopwatch.models.core.Person)))])), ('organisation_listing', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock()), ('organisations', wagtail.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(stopwatch.models.core.Organisation)))])), ('alert', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock()), ('content', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link']))])), ('calendar', wagtail.blocks.StructBlock([('site_area', wagtail.blocks.PageChooserBlock(help_text='Show all events in the site that are under this page. If blank, show all events on the site.', required=False))])), ('accordion', wagtail.blocks.StreamBlock([('richtext', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Title')), ('content', wagtail.blocks.RichTextBlock())])), ('people', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Title')), ('content', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('people', wagtail.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(stopwatch.models.core.Person)))]))]))]))], blank=True, use_json_field=None),
        ),
        migrations.AlterField(
            model_name='form',
            name='thank_you_page',
            field=wagtail.fields.StreamField([('text', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'])), ('embed', wagtail.blocks.StructBlock([('embed_url', wagtail.blocks.URLBlock()), ('fullscreen', wagtail.blocks.BooleanBlock(default=False, required=False))])), ('downloads', wagtail.blocks.StructBlock([('documents', wagtail.blocks.ListBlock(wagtail.documents.blocks.DocumentChooserBlock()))])), ('cta', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'], required=False)), ('target', wagtail.blocks.PageChooserBlock(required=True))])), ('form', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'], required=False)), ('target', wagtail.blocks.PageChooserBlock('stopwatch.Form', required=True))])), ('links', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('message', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'], required=False)), ('links', wagtail.blocks.StreamBlock([('alert', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock()), ('content', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link']))])), ('website', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock()), ('name', wagtail.blocks.CharBlock(required=False))])), ('email', wagtail.blocks.StructBlock([('address', wagtail.blocks.EmailBlock()), ('name', wagtail.blocks.CharBlock(required=False))])), ('page', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock()), ('name', wagtail.blocks.CharBlock(required=False))]))]))])), ('newsletter_signup', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'], required=False)), ('target', wagtail.blocks.PageChooserBlock(required=True))])), ('person_listing', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('people', wagtail.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(stopwatch.models.core.Person)))])), ('organisation_listing', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock()), ('organisations', wagtail.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(stopwatch.models.core.Organisation)))])), ('alert', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock()), ('content', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link']))])), ('calendar', wagtail.blocks.StructBlock([('site_area', wagtail.blocks.PageChooserBlock(help_text='Show all events in the site that are under this page. If blank, show all events on the site.', required=False))])), ('accordion', wagtail.blocks.StreamBlock([('richtext', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Title')), ('content', wagtail.blocks.RichTextBlock())])), ('people', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Title')), ('content', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('people', wagtail.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(stopwatch.models.core.Person)))]))]))]))], use_json_field=None),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='body',
            field=wagtail.fields.StreamField([('text', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'])), ('embed', wagtail.blocks.StructBlock([('embed_url', wagtail.blocks.URLBlock()), ('fullscreen', wagtail.blocks.BooleanBlock(default=False, required=False))])), ('downloads', wagtail.blocks.StructBlock([('documents', wagtail.blocks.ListBlock(wagtail.documents.blocks.DocumentChooserBlock()))])), ('cta', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'], required=False)), ('target', wagtail.blocks.PageChooserBlock(required=True))])), ('form', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'], required=False)), ('target', wagtail.blocks.PageChooserBlock('stopwatch.Form', required=True))])), ('links', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('message', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'], required=False)), ('links', wagtail.blocks.StreamBlock([('alert', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock()), ('content', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link']))])), ('website', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock()), ('name', wagtail.blocks.CharBlock(required=False))])), ('email', wagtail.blocks.StructBlock([('address', wagtail.blocks.EmailBlock()), ('name', wagtail.blocks.CharBlock(required=False))])), ('page', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock()), ('name', wagtail.blocks.CharBlock(required=False))]))]))])), ('newsletter_signup', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('content', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'], required=False)), ('target', wagtail.blocks.PageChooserBlock(required=True))])), ('person_listing', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('people', wagtail.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(stopwatch.models.core.Person)))])), ('organisation_listing', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock()), ('organisations', wagtail.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(stopwatch.models.core.Organisation)))])), ('alert', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock()), ('content', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link']))])), ('calendar', wagtail.blocks.StructBlock([('site_area', wagtail.blocks.PageChooserBlock(help_text='Show all events in the site that are under this page. If blank, show all events on the site.', required=False))])), ('accordion', wagtail.blocks.StreamBlock([('richtext', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Title')), ('content', wagtail.blocks.RichTextBlock())])), ('people', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Title')), ('content', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('people', wagtail.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(stopwatch.models.core.Person)))]))]))])), ('articles_list', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock()), ('site_area', wagtail.blocks.PageChooserBlock(page_type=['stopwatch.Category'])), ('style', wagtail.blocks.ChoiceBlock(choices=[('GRID', 'Grid'), ('ROWS', 'Rows')]))]))], blank=True, use_json_field=None),
        ),
        migrations.CreateModel(
            name='MultiPageSnippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('pages', modelcluster.fields.ParentalManyToManyField(blank=True, to='wagtailcore.Page')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='pinned_pages_style',
            field=models.CharField(choices=[('grid', 'Grid'), ('rows', 'Rows')], default='grid', max_length=10),
        ),
        migrations.AddField(
            model_name='category',
            name='pinned_pages',
            field=wagtail.fields.StreamField([('pinned_page', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock(help_text='Show all events in the site that are under this page. If blank, show all events on the site.', required=False))]))], blank=True, use_json_field=None),
        ),
    ]
