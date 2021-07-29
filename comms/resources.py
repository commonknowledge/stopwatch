from datetime import datetime, timezone
import json
import logging
import re

from django.core.exceptions import ObjectDoesNotExist
from wagtail.core.rich_text import RichText
from stopwatch.models import StopWatchDocument, StopwatchImage
from import_export import resources, widgets, fields

from comms import models


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
            (type, coerce_streamfield_value(type, value))
            for type, value
            in cleaned_value
            if coerce_streamfield_value(type, value) is not None
            and value != ''
        ]

    def render(self, value, obj=None):
        return str(value)


class TextToStreamWidget(widgets.Widget):
    def clean(self, value: str, *args, **kwargs):
        if not value:
            return []

        return [
            ('text', coerce_streamfield_value('text', f'<p>{value}</p>'))
        ]

    def render(self, value, obj=None):
        return str(value)


class NewsItemResource(resources.ModelResource):
    class Meta:
        model = models.NewsItem
        fields = ('import_ref', 'title',
                  'intro_text', 'body', 'photo', 'summary', 'slug', 'first_published_at')
        import_id_fields = ('import_ref',)

    first_published_at = fields.Field(widget=TimestampWidget())

    photo = fields.Field(widget=ImageWidget(),
                         attribute='photo', column_name='photo')

    body = fields.Field(widget=StreamWidget(),
                        attribute='body', column_name='body')

    summary = fields.Field(widget=TextToStreamWidget(),
                           attribute='summary', column_name='intro_text')

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent

    def before_save_instance(self, instance, *args, **kwargs):
        if instance is not None:
            self.parent.add_child(instance=instance)

    def import_field(self, field, obj, data, *args):
        if field.column_name != 'parent':
            return super().import_field(field, obj, data, *args)


def coerce_streamfield_value(type, value):
    if value is None:
        return None

    if type == 'text':
        return RichText(value)

    elif type == 'document':
        return resolve_document(value)

    raise TypeError(f'Unhandled type: {type}')


def resolve_document(value):
    if not value:
        return

    value = re.sub(r'{filedir_(\d+)}',
                   lambda match: f'import_{match.group(1)}_',
                   value)

    try:
        if value.lower().endswith('.pdf'):
            return StopWatchDocument.objects.get(import_ref=value)
        else:
            return StopwatchImage.objects.get(import_ref=value)
    except ObjectDoesNotExist:
        logging.error('Document not found: %s', value)
        return None
