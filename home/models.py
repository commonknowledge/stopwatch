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

from widgets.models import ArticlesListBlock, CtaBlock, NewsletterSignupBlock, TabsBlock


class ListPage(Page):
    page_description = models.CharField(max_length=512, default='')
    landing_video = models.URLField(blank=True, null=True)

    body = StreamField([
        ('articles_list', ArticlesListBlock()),
        ('cta', CtaBlock()),
        ('tabs', TabsBlock()),
        ('newsletter_signup', NewsletterSignupBlock())
    ], min_num=0, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('page_description'),
        FieldPanel('landing_video'),
        StreamFieldPanel('body'),
    ]

    @property
    def featured_items(self):
        return get_children_of_type(self, NewsItem).filter(photo__isnull=False)[:10]


class ExternalPage(Page):
    target_url = URLField()

    content_panels = Page.content_panels + [
        FieldPanel('target_url'),
    ]

    def serve(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.target_url)
