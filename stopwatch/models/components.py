from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from django.http.request import HttpRequest
from commonknowledge.helpers import safe_to_int
from stopwatch.models.core import Organisation, Person
from django.utils.html import format_html
from wagtail.core.blocks.field_block import BooleanBlock, ChoiceBlock, EmailBlock, MultipleChoiceBlock, TextBlock, URLBlock
from wagtail.core.blocks.list_block import ListBlock
from wagtail.core.blocks.stream_block import StreamBlock
from wagtail.core.blocks import StructBlock, RichTextBlock, CharBlock, PageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from stopwatch.models.fields import IconFieldBlock


class AlertBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/alert.html'

    heading = CharBlock()
    content = RichTextBlock(
        features=['bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', ])


class LinksBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/links.html'

    class LinkBlock(StructBlock):
  
        def __init__(self, tag, link_block, **kwargs):
            local_blocks = (
                (tag, link_block),
                ('name', CharBlock(required=False)), 

            )
            super().__init__(local_blocks=local_blocks, **kwargs)
            self.tag = tag

        def get_target(self, value):
            return value[self.tag]

        def get_href(self, value):
            return str(self.get_target(value))

        def get_label(self, value):
            return value.get('name', str(self.get_target(value)))

        def get_link(self, value):
            return format_html('<a href="{}">{}</a>', self.get_href(value), self.get_label(value))

        def get_context(self, value, parent_context):
            context = super().get_context(value, parent_context=parent_context)
            context['link'] = self.get_link(value)
            return context

    class MailtoLinkBlock(LinkBlock):
        class Meta:
            template = 'stopwatch/components/email_link.html'
        def get_href(self, value):
            return 'mailto:' + super().get_href(value)

    class InternalPageLinkBlock(LinkBlock):
        class Meta:
            template = 'stopwatch/components/internal_link.html'
        def get_href(self, value):
            return self.get_target(value).url
    
    class ExternalPageLinkBlock(LinkBlock):
        class Meta:
            template = 'stopwatch/components/external_link.html'
        def get_href(self, value):
            return self.get_target(value)

    heading = CharBlock(required=False)
    message = RichTextBlock(required=False, features=['h1', 'h2', 'h3', 'h4', 'bold',
                                                      'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'])
    links = StreamBlock((
        ('alert', AlertBlock()),
        ('website', ExternalPageLinkBlock('url', URLBlock())),
        ('email', MailtoLinkBlock('address', EmailBlock())),
        ('page', InternalPageLinkBlock('page', PageChooserBlock()))
    ))

    def get_context(self, value, *args, **kwargs):
        context = super().get_context(value, *args, **kwargs)

        if value.get('site_area') is not None:
            context['qs'] = value['site_area'].featured_items

        return context


class ArticlesListBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/articles_list.html'

    class StyleChoices:
        GRID = 'GRID'
        ROWS = 'ROWS'

        options = (
            (GRID, 'Grid'),
            (ROWS, 'Rows'),
        )

    heading = CharBlock()
    site_area = PageChooserBlock(page_type='stopwatch.Category')
    style = ChoiceBlock(
        choices=StyleChoices.options,
        default=StyleChoices.ROWS)

    def get_context(self, value, *args, **kwargs):
        context = super().get_context(value, *args, **kwargs)

        if value.get('site_area') is not None:
            context['qs'] = value['site_area'].featured_items

        return context


class CalendarBlock(StructBlock):
    '''
    Display a calendar showing all events underneath a particular page.
    '''

    class Meta:
        template = 'stopwatch/components/calendar.html'
        help_text = ''

    site_area = PageChooserBlock(
        required=False,
        help_text="Show all events in the site that are under this page. If blank, show all events on the site."
    )

    def get_context(self, value, *args, **kwargs):
        from projects.models import Event
        parent_context = kwargs['parent_context']
        block_id = get_block_id(
            parent_context['page'].body,
            value,
            prefix='calendar'
        )

        request: HttpRequest = parent_context['request']
        today = date.today()
        month = safe_to_int(request.GET.get(
            f'{block_id}-month'), today.month)
        year = safe_to_int(request.GET.get(
            f'{block_id}-year'), today.year)

        context = super().get_context(value, *args, **kwargs)
        site_area = value.get('site_area')

        if site_area:
            events = Event.objects.descendant_of(site_area)
        else:
            events = Event.objects.all()

        events = events.filter(
            start_time__gte=datetime(year, month, 1),
            start_time__lt=datetime(year, month, 1) + relativedelta(months=1)
        ).order_by('start_time').live()

        context['events'] = events
        context['year'] = year
        context['month'] = month
        context['month_name'] = date(year, month, 1).strftime('%B')
        context['block_id'] = block_id
        context['url'] = request.get_full_path()

        return context


class PullQuoteBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/pull_quote.html'

    quote = TextBlock()


class EmbedBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/embed.html'

    embed_url = URLBlock()
    fullscreen = BooleanBlock(default=False, required=False)


class DownloadsBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/downloads.html'

    documents = ListBlock(DocumentChooserBlock())


class CtaBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/cta.html'

    heading = CharBlock(required=False)
    image = ImageChooserBlock(required=False)
    content = RichTextBlock(required=False, features=['h1', 'h2', 'h3', 'h4', 'bold',
                                                      'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'])
    target = PageChooserBlock(required=True)


class PersonListBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/person_list.html'

    heading = CharBlock(required=False)
    people = ListBlock(SnippetChooserBlock(Person))

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        # We want to render differently if just a single person in the list (full-width on desktop-size screens)
        if len(value['people']) == 1:
            context['single_person_list'] = True

        return context


class OrganisationListBlock(StructBlock):
    class Meta:
        template = 'stopwatch/components/organisation_list.html'

    heading = CharBlock()
    organisations = ListBlock(SnippetChooserBlock(Organisation))


class NewsletterSignupBlock(CtaBlock):
    class Meta:
        template = 'stopwatch/components/newsletter_signup.html'

    heading = CharBlock(required=False)
    image = ImageChooserBlock(required=False)
    content = RichTextBlock(required=False, features=['h1', 'h2', 'h3', 'h4', 'bold',
                                                      'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'])


class FormBlock(CtaBlock):
    class Meta:
        template = 'stopwatch/components/form.html'

    target = PageChooserBlock('stopwatch.Form', required=True)

    def get_context(self, value, *args, **kwargs):
        from stopwatch.models.pages import Form

        context = super().get_context(value, *args, **kwargs)
        target = value.get('target', None)

        if target and issubclass(target.specific_class, Form):
            context['form'] = target.specific.get_form(page=self, user=None)

        return context


class SummaryTextBlock(RichTextBlock):
    features = ['bold', 'italic', 'ol', 'ul',
                'link', 'document-link', 'blockquote']


class AccordionStreamBlock(StreamBlock):
    """
    Accordion content block
    """
    required = True
    richtext = StructBlock([
        ('title', CharBlock(
            label='Title',
        )),
        ('content', RichTextBlock()),
    ])
    people = StructBlock([
        ('title', CharBlock(
            label='Title',
        )),
        ('content', PersonListBlock()),
    ])

    class Meta:
        icon = 'folder-open-1'
        template = 'stopwatch/components/accordion_block.html'
        label = 'Accordion'


TEXT_MODULES = (
    ('text', RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold',
     'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'blockquote'])),
    # ('quote', PullQuoteBlock()), # NB: there may be historical uses of this, even though it is removed
    ('embed', EmbedBlock()),
    ('downloads', DownloadsBlock()),


)

CONTENT_MODULES = TEXT_MODULES + (
    ('cta', CtaBlock()),
    ('form', FormBlock()),
    ('links', LinksBlock()),
    ('newsletter_signup', NewsletterSignupBlock()),
    ('person_listing', PersonListBlock()),
    ('organisation_listing', OrganisationListBlock()),
    ('alert', AlertBlock()),
    ('calendar', CalendarBlock()),
    ('accordion', AccordionStreamBlock())
)

LANDING_MODULES = CONTENT_MODULES + (
    ('articles_list', ArticlesListBlock()),
)


def get_block_id(stream, value, prefix):
    i = 0

    for x in stream:
        if x.value == value:
            return prefix if i == 0 else f'{prefix}-{i}'

        i += 1

    return None
