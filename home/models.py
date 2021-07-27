from comms.models import NewsItem
from commonknowledge.wagtail.helpers import get_children_of_type
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from commonknowledge.wagtail.models import ChildListMixin

from widgets.models import ArticlesListBlock, CtaBlock, NewsletterSignupBlock


class ListPage(Page):
    body = StreamField([
        ('articles_list', ArticlesListBlock()),
        ('cta', CtaBlock()),
        ('newsletter_signup', NewsletterSignupBlock())
    ], min_num=0, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    @property
    def featured_items(self):
        return get_children_of_type(self, NewsItem).filter(photo__isnull=False)[:10]
