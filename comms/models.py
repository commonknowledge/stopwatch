from stopwatch.models import StopwatchImage
from django.db import models

from wagtail.images.models import Image
from wagtail.core.models import Page
from wagtail.core import fields


class CommsPage(Page):
    class Meta:
        abstract = True

    import_ref = models.IntegerField(null=True, blank=True)
    photo = models.ForeignKey(
        StopwatchImage, null=True, blank=True, on_delete=models.SET_NULL)


class NewsItem(CommsPage):
    intro_text = fields.RichTextField(blank=True)
    content = fields.RichTextField(blank=True)
