from django.db.models.fields import URLField
from wagtail.core.blocks.field_block import URLBlock
from comms.models import NewsItem
from commonknowledge.wagtail.helpers import get_children_of_type
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from django.http.response import HttpResponseRedirect
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from commonknowledge.wagtail.models import ChildListMixin

from widgets.models import COMMON_MODULES


class LandingPage(Page):
    page_description = models.CharField(max_length=512, default='')
    landing_video = models.URLField(blank=True, null=True)

    body = StreamField(COMMON_MODULES, min_num=0, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('page_description'),
        FieldPanel('landing_video'),
        StreamFieldPanel('body'),
    ]


class ListPage(ChildListMixin, Page):
    class StyleChoices:
        COMPACT = 'COMPACT'
        EXPANDED = 'EXPANDED'

        options = (
            (COMPACT, 'Compact'),
            (EXPANDED, 'Expanded')
        )

    searchable = models.BooleanField(default=False)
    newsflash = models.BooleanField(default=False)
    style = models.CharField(choices=StyleChoices.options,
                             max_length=128, default=StyleChoices.COMPACT)

    content_panels = Page.content_panels + [
        FieldPanel('searchable'),
        FieldPanel('newsflash'),
        FieldPanel('style'),
    ]

    def get_page_size(self):
        if self.style == ListPage.StyleChoices.COMPACT:
            return 100
        else:
            return 25

    @property
    def featured_items(self):
        return get_children_of_type(self, NewsItem).filter(photo__isnull=False).order_by('-first_published_at')[:10]


class ExternalPage(Page):
    target_url = URLField()

    content_panels = Page.content_panels + [
        FieldPanel('target_url'),
    ]

    def serve(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.target_url)
