from datetime import datetime, timezone
import json
import logging
import re
from urllib import parse
from stopwatch.models.pages import Article

from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from wagtail.core.rich_text import RichText
from stopwatch.models import StopWatchDocument, StopwatchImage
from import_export import resources, widgets, fields

from stopwatch import models


class ImageWidget(widgets.Widget):
    def clean(self, value: str, *args, **kwargs):
        return resolve_document(value)

    def render(self, value, obj=None):
        if not value:
            return

        try:
            return value.file.url
        except NotImplementedError:
            pass


class TimestampWidget(widgets.Widget):
    def clean(self, value: str, *args, **kwargs):
        if value:
            return datetime.fromtimestamp(float(value), timezone.utc)

    def render(self, value, obj=None):
        return str(value)


class StreamWidget(widgets.Widget):
    def clean(self, value: str, *args, **kwargs):
        if not value:
            return []

        value = json.loads(value)

        cleaned_value = (x for x in value if x is not None)

        return [
            coerce_streamfield_value(type, value)
            for type, value
            in cleaned_value
            if coerce_streamfield_value(type, value) is not None
            and value != ''
        ]

    def render(self, value, obj=None):
        return str(obj)


class TextToStreamWidget(widgets.Widget):
    def clean(self, value: str, *args, **kwargs):
        if not value:
            return []

        return [
            coerce_streamfield_value('text', f'<p>{value}</p>')
        ]

    def render(self, value, obj=None):
        return str(value)


class ArticleResource(resources.ModelResource):
    class Meta:
        model = models.Article
        fields = ('import_ref', 'title',
                  'intro_text', 'body', 'photo', 'summary', 'slug', 'first_published_at')
        import_id_fields = ('import_ref',)

    first_published_at = fields.Field(widget=TimestampWidget(
    ), attribute='first_published_at', column_name='first_published_at')

    photo = fields.Field(widget=ImageWidget(),
                         attribute='photo', column_name='photo')

    body = fields.Field(widget=StreamWidget(),
                        attribute='body', column_name='body')

    summary = fields.Field(widget=TextToStreamWidget(),
                           attribute='summary', column_name='intro_text')

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent

    def after_import(self, dataset, result, *args, **kwargs):
        for page in result.rows:
            if page.import_type in ('new', 'update'):
                fixup_article_html(Article.objects.get(pk=page.object_id))

        super().after_import(dataset, result, *args, **kwargs)

    def before_save_instance(self, instance, *args, **kwargs):
        if instance is not None and instance.get_parent() is None:
            self.parent.add_child(instance=instance)

    def import_field(self, field, obj, data, *args):
        if field.column_name != 'parent':
            return super().import_field(field, obj, data, *args)


def coerce_streamfield_value(type, value):
    if value is None:
        return None

    if type == 'text':
        return 'text', RichText(fixup_html(value))

    elif type == 'document':
        return 'downloads', {
            'title': 'Downloads',
            'documents': [resolve_document(value)]
        }

    raise TypeError(f'Unhandled type: {type}')


def fixup_article_html(article):
    for block in article.body:
        if block.block_type == 'text':
            block.value = RichText(post_fixup_html(block.value.source))

    article.save()


def fixup_html(html):
    doc = BeautifulSoup(html, 'html.parser')

    for img in doc.find_all('img'):
        try:
            image_obj = StopwatchImage.objects.get(
                import_ref=fixup_img_src(img['src']))
        except StopwatchImage.DoesNotExist:
            img.decompose()
            continue

        img.name = 'embed'
        img.attrs = {
            'embedtype': 'image',
            'format': 'fullwidth',
            'id': image_obj.id
        }

    for a in doc.find_all('a'):
        href = a.attrs.get('href', None)

        if href is None:
            a.unwrap()
            continue

        if re.match(r'https?://(www\.)?stop-watch\.org', href):
            a.attrs = {
                'linktype': 'page',
                'import_path': re.search(r'stop-watch\.org/(.*)', href).group(1).rstrip('/')
            }

        elif href.startswith('{'):
            a.attrs = {
                'linktype': 'page',
                'import': re.search(r'\d+', href).group(0)
            }

    return str(doc)


def post_fixup_html(html):
    doc = BeautifulSoup(html, 'html.parser')

    for a in doc.find_all('a'):
        if 'import' not in a.attrs:
            continue

        try:
            hit = Article.objects.get(import_ref=int(a['import']))
            a['id'] = hit.id
            del a['import']
        except Article.DoesNotExist:
            pass

    return str(doc)


def resolve_document(value):
    if not value:
        return

    value = fixup_img_src(value)

    try:

        if re.match(r'.*\.(pdf|doc|docx|csv|rtf|txt)$', value.lower()):
            return StopWatchDocument.objects.get(import_ref=value)
        else:
            return StopwatchImage.objects.get(import_ref=value)
    except ObjectDoesNotExist:
        logging.error('Document not found: %s', value)
        return None


def fixup_img_src(value):
    src = re.sub(r'{filedir_(\d+)}',
                 lambda match: f'import_{match.group(1)}_',
                 value)

    return parse.unquote(src)
