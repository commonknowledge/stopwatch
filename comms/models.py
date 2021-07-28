from widgets.models import COMMON_MODULES, TEXT_MODULES
from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core import fields

from stopwatch.models import StopwatchImage


class CommsPage(Page):
    class Meta:
        abstract = True

    import_ref = models.IntegerField(null=True, blank=True)
    photo = models.ForeignKey(
        StopwatchImage, null=True, blank=True, on_delete=models.SET_NULL)


class NewsItem(CommsPage):
    intro_text = fields.RichTextField(blank=True)
    summary = fields.StreamField(TEXT_MODULES, min_num=0, blank=True)
    body = fields.StreamField(COMMON_MODULES, min_num=0, blank=True)

    content_panels = CommsPage.content_panels + [
        FieldPanel('intro_text'),
        FieldPanel('body')
    ]
