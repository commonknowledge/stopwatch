from wagtail.core.blocks.field_block import ChoiceBlock
from wagtail.core.blocks.stream_block import StreamBlock
from wagtail.core.blocks import StructBlock, RichTextBlock, CharBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock


def IconBlock(**kwargs):
    return ChoiceBlock(
        choices=(
            ('chat-left', 'Speech Bubble'),
            ('grap-up', 'Graph'),
            ('hammer', 'Gavel'),
        ),
        template='widgets/icon_block.html',
        **kwargs
    )


class TabsBlock(StructBlock):
    class Meta:
        template = 'widgets/tabs_block.html'

    class BaseTab(StructBlock):
        icon = IconBlock()
        short_title = CharBlock()
        title = CharBlock()
        call_to_action = CharBlock(required=False)
        related_page = PageChooserBlock(required=False)

    class StatsTab(BaseTab):
        class Meta:
            template = 'widgets/tab/stats.html'

    class InfoTab(BaseTab):
        class Meta:
            template = 'widgets/tab/info.html'

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
        template = 'widgets/articles_list_block.html'

    heading = CharBlock()
    image = ImageChooserBlock(required=False)
    site_area = PageChooserBlock(page_type='home.ListPage')

    def get_context(self, value, *args, **kwargs):
        context = super().get_context(value, *args, **kwargs)

        context['qs'] = value['site_area'].featured_items

        return context


class CtaBlock(StructBlock):
    class Meta:
        template = 'widgets/cta_block.html'

    heading = CharBlock()
    image = ImageChooserBlock(required=False)
    content = RichTextBlock()
    target = PageChooserBlock(required=False)


class NewsletterSignupBlock(CtaBlock):
    class Meta:
        template = 'widgets/newsletter_block.html'


TEXT_MODULES = (
    ('text', RichTextBlock()),
)

COMMON_MODULES = TEXT_MODULES + (
    ('articles_list', ArticlesListBlock()),
    ('cta', CtaBlock()),
    ('tabs', TabsBlock()),
    ('newsletter_signup', NewsletterSignupBlock()),
)
