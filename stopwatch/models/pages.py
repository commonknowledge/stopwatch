from django.db.models.fields import URLField
from wagtail.core.blocks.field_block import URLBlock
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from django.http.response import HttpResponseRedirect
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from commonknowledge.wagtail.helpers import get_children_of_type
from commonknowledge.wagtail.models import ChildListMixin

from stopwatch.models.core import StopwatchImage
from stopwatch.models.components import COMMON_MODULES, TEXT_MODULES


class LandingPage(Page):
    template = 'stopwatch/pages/landing.html'

    page_description = models.CharField(max_length=512, default='')
    landing_video = models.URLField(blank=True, null=True)

    body = StreamField(COMMON_MODULES, min_num=0, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('page_description'),
        FieldPanel('landing_video'),
        StreamFieldPanel('body'),
    ]


class Article(Page):
    template = 'stopwatch/pages/article.html'

    import_ref = models.IntegerField(null=True, blank=True)
    photo = models.ForeignKey(
        StopwatchImage, null=True, blank=True, on_delete=models.SET_NULL)

    intro_text = models.CharField(max_length=1024, default='', blank=True)
    summary = StreamField(TEXT_MODULES, min_num=0, blank=True)
    body = StreamField(COMMON_MODULES, min_num=0, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro_text'),
        FieldPanel('summary'),
        FieldPanel('body')
    ]


class Category(ChildListMixin, Page):
    template = 'stopwatch/pages/category.html'

    class StyleChoices:
        COMPACT = 'COMPACT'
        EXPANDED = 'EXPANDED'

        options = (
            (COMPACT, 'Compact'),
            (EXPANDED, 'Expanded')
        )

    photo = models.ForeignKey(
        StopwatchImage, null=True, blank=True, on_delete=models.SET_NULL)
    searchable = models.BooleanField(default=False)
    newsflash = models.BooleanField(default=False)
    style = models.CharField(choices=StyleChoices.options,
                             max_length=128, default=StyleChoices.COMPACT)

    content_panels = Page.content_panels + [
        ImageChooserPanel('photo'),
        FieldPanel('searchable'),
        FieldPanel('newsflash'),
        FieldPanel('style'),
    ]

    def get_page_size(self):
        if self.style == Category.StyleChoices.COMPACT:
            return 100
        else:
            return 25

    @property
    def featured_items(self):
        return get_children_of_type(self, Article).filter(photo__isnull=False).order_by('-first_published_at')[:10]


class ExternalPage(Page):
    target_url = URLField()

    content_panels = Page.content_panels + [
        FieldPanel('target_url'),
    ]

    def serve(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.target_url)
