from django.utils.safestring import mark_safe
from wagtail.core.blocks.field_block import TextBlock, URLBlock
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
        author = SnippetChooserBlock('stopwatch.StaffMember', required=False)

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


class EmbedBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/embed.html'

    embed_url = URLBlock()


class CtaBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/cta.html'

    heading = CharBlock()
    image = ImageChooserBlock(required=False)
    content = RichTextBlock()
    target = PageChooserBlock(required=False)


class NewsletterSignupBlock(CtaBlock):
    class Meta:
        template = 'stopwatch/components/newsletter_signup.html'


TEXT_MODULES = (
    ('text', RichTextBlock()),
    ('embed', EmbedBlock()),
    ('document', DocumentChooserBlock()),
)

COMMON_MODULES = TEXT_MODULES + (
    ('articles_list', ArticlesListBlock()),
    ('cta', CtaBlock()),
    ('tabs', TabsBlock()),
    ('newsletter_signup', NewsletterSignupBlock()),
)
