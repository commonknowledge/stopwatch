
from stopwatch.models.core import Person
from django.utils.html import format_html
from wagtail.core.blocks.field_block import BooleanBlock, EmailBlock, TextBlock, URLBlock
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


class AlertBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/alert.html'

    heading = CharBlock()
    content = TextBlock()


class LinksBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/links.html'

    class LinkBlock(StructBlock):
        class Meta:
            template = 'stopwatch/components/links_link.html'

        name = CharBlock()
        description = TextBlock(required=False)

        def __init__(self, tag, link_block, **kwargs):
            local_blocks = (
                (tag, link_block),
            )
            super().__init__(local_blocks=local_blocks, **kwargs)
            self.tag = tag

        def get_target(self, value):
            return value[self.tag]

        def get_href(self, value):
            return str(self.get_target(value))

        def get_label(self, value):
            return str(self.get_target(value))

        def get_link(self, value):
            return format_html('<a href="{}">{}</a>', self.get_href(value), self.get_label(value))

        def get_context(self, value, parent_context):
            context = super().get_context(value, parent_context=parent_context)
            context['link'] = self.get_link(value)
            return context

    class MailtoLinkBlock(LinkBlock):
        def get_href(self, value):
            return 'mailto:' + super().get_href(value)

    class InternalLinkBlock(LinkBlock):
        def get_href(self, value):
            return self.get_target(value).url

    heading = CharBlock()
    message = RichTextBlock(required=False)
    links = StreamBlock((
        ('alert', AlertBlock()),
        ('website', LinkBlock('url', URLBlock())),
        ('email', MailtoLinkBlock('address', EmailBlock())),
        ('page', InternalLinkBlock('page', PageChooserBlock()))
    ))

    def get_context(self, value, *args, **kwargs):
        context = super().get_context(value, *args, **kwargs)

        if value.get('site_area') is not None:
            context['qs'] = value['site_area'].featured_items

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


class PersonListBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/person_list.html'

    heading = CharBlock()
    people = ListBlock(SnippetChooserBlock(Person))


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
    ('links', LinksBlock()),
    ('newsletter_signup', NewsletterSignupBlock()),
    ('person_listing', PersonListBlock()),
    ('alert', AlertBlock())
)

LANDING_MODULES = CONTENT_MODULES + (
    ('articles_list', ArticlesListBlock()),
    ('tabs', TabsBlock()),
)
