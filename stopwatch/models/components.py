from django.utils.safestring import mark_safe
from wagtail.core.blocks.field_block import BooleanBlock, TextBlock, URLBlock
from wagtail.core.blocks.list_block import ListBlock
from wagtail.core.blocks.stream_block import StreamBlock
from wagtail.core.blocks import StructBlock, RichTextBlock, CharBlock, PageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from stopwatch.models.fields import IconFieldBlock


class TabsBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/tabs.html'

    class BaseTab(StructBlock):
        icon = IconFieldBlock()
        short_title = CharBlock()
        title = CharBlock()
        call_to_action = CharBlock(required=False)
        related_page = PageChooserBlock(required=False)

    class StatsTab(BaseTab):
        class Meta:
            template = 'stopwatch/tabs/stats.html'

    class InfoTab(BaseTab):
        class Meta:
            template = 'stopwatch/tabs/info.html'

        content = RichTextBlock()
        author = SnippetChooserBlock('stopwatch.Person', required=False)

    heading = CharBlock()
    tabs = StreamBlock([
        ('stats', StatsTab()),
        ('info', InfoTab()),
    ])

    def get_context(self, value, *args, **kwargs):
        context = super().get_context(value, *args, **kwargs)
        tabs = value['tabs']
        context['tab_data'] = [{'meta': tab['value'], 'tab': tabs[idx]}
                               for idx, tab in enumerate(tabs.raw_data)]

        return context


class ArticlesListBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/articles_list.html'

    heading = CharBlock()
    site_area = PageChooserBlock(page_type='stopwatch.Category')

    def get_context(self, value, *args, **kwargs):
        context = super().get_context(value, *args, **kwargs)

        if value.get('site_area') is not None:
            context['qs'] = value['site_area'].featured_items

        return context


class PullQuoteBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/pull_quote.html'

    quote = TextBlock()


class EmbedBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/embed.html'

    embed_url = URLBlock()
    fullscreen = BooleanBlock(default=False)


class DownloadsBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/downloads.html'

    title = CharBlock(required=False)
    documents = ListBlock(DocumentChooserBlock())


class CtaBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/cta.html'

    heading = CharBlock(required=False)
    image = ImageChooserBlock(required=False)
    content = RichTextBlock(required=False)
    target = PageChooserBlock(required=True)

    def get_context(self, value, *args, **kwargs):
        from stopwatch.models.pages import Form

        context = super().get_context(value, *args, **kwargs)
        target = value.get('target', None)

        if target and issubclass(target.specific_class, Form):
            context['form'] = target.specific.get_form(page=self, user=None)

        return context


class NewsletterSignupBlock(CtaBlock):
    class Meta:
        template = 'stopwatch/components/newsletter_signup.html'


TEXT_MODULES = (
    ('text', RichTextBlock()),
    ('quote', PullQuoteBlock()),
    ('embed', EmbedBlock()),
    ('downloads', DownloadsBlock()),
)

CONTENT_MODULES = TEXT_MODULES + (
    ('cta', CtaBlock()),
    ('newsletter_signup', NewsletterSignupBlock()),
)

LANDING_MODULES = CONTENT_MODULES + (
    ('articles_list', ArticlesListBlock()),
    ('tabs', TabsBlock()),
)
