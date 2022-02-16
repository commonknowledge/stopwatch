from django.db.models.fields.related import ForeignKey
from wagtail.core.blocks.field_block import CharBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock
from stopwatch.models.mixins import ListableMixin
from django.db.models.fields import URLField
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.core.blocks import StructBlock, PageChooserBlock
from wagtail.core.blocks.stream_block import StreamBlock
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core.fields import RichTextField, StreamField
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from taggit.models import Tag, TaggedItemBase
from commonknowledge.wagtail.helpers import get_children_of_type
from commonknowledge.wagtail.models import ChildListMixin
from commonknowledge.django.cache import django_cached
from commonknowledge.helpers import classproperty

from wagtailmetadata.models import MetadataPageMixin

from stopwatch.models.core import Person, SiteSettings, StopwatchImage
from stopwatch.models.components import CONTENT_MODULES, TEXT_MODULES, LANDING_MODULES, ArticlesListBlock


class ArticleTag(TaggedItemBase):
    content_object = ParentalKey(
        'Article', on_delete=models.CASCADE, related_name='tagged_items')


class StopwatchPage(MetadataPageMixin, Page):
    class Meta:
        abstract = True

    hide_date = True

    photo = models.ForeignKey(
        StopwatchImage, null=True, blank=True, on_delete=models.SET_NULL)

    show_header_image = models.BooleanField(default=True)

    @property
    def category(self):
        return Category.objects.ancestor_of(self, inclusive=True).last()

    @classmethod
    def get_display_options(cls):
        return [
            FieldPanel('show_header_image')
        ]

    @classproperty
    def settings_panels(cls):
        return Page.settings_panels + [
            MultiFieldPanel(cls.get_display_options(), 'Display Options')
        ]


class LandingPage(StopwatchPage):
    template = 'stopwatch/pages/landing.html'
    parent_page_types = ('wagtailcore.Page',)

    class Tab(StructBlock):
        site_area = PageChooserBlock()
        featured_page = PageChooserBlock(required=False)
        image = ImageChooserBlock(required=False)
        title = CharBlock(required=False)
        heading = CharBlock(required=False, label='Detail heading')
        description = TextBlock(required=False, label='Detail description')
        cta = CharBlock(required=False, label='Call to action text')

    page_description = models.CharField(
        max_length=128, default="Research and action for fair and accountable policing")
    newsflash_category = models.ForeignKey(
        'stopwatch.Category', null=True, blank=True, on_delete=models.SET_NULL)

    tabs = StreamField([
        ('tab', Tab()),
    ], max_num=4, blank=True)

    body = StreamField(LANDING_MODULES, min_num=0, blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('photo'),
        PageChooserPanel('newsflash_category'),
        StreamFieldPanel('tabs'),
        StreamFieldPanel('body'),
    ]

    @property
    def tab_data(self):
        if len(self.tabs.raw_data) == 0:
            return

        return [
            {
                'meta': self.get_landing_tab_data(**tab['value']),
                'tab': self.tabs[idx]
            }
            for idx, tab in enumerate(self.tabs.raw_data)
        ]

    def get_landing_tab_data(self, site_area, featured_page, title, cta, heading=None, description=None, image=None, **kwargs):
        site_area = Page.objects.get(pk=site_area).specific
        if featured_page:
            featured_page = Page.objects.get(pk=featured_page).specific

        elif hasattr(site_area, 'featured_items') and len(site_area.featured_items) > 0:
            featured_page = site_area.featured_items[0]

        else:
            featured_page = site_area.get_children().specific().first()

        if description is None or description == '':
            if featured_page is not None:
                description = featured_page.intro_text

        if image is None:
            if featured_page is not None:
                image = featured_page.photo
            else:
                image = site_area.photo
        elif isinstance(image, int):
            image = StopwatchImage.objects.filter(pk=image).first()

        if heading is None or heading == '':
            if featured_page:
                heading = featured_page.title

        return {
            'title': title or site_area.title,
            'url': site_area.url,
            'page': featured_page,
            'photo': image,
            'heading': heading,
            'cta': cta or site_area.title,
            'description': description,
            'short_description': site_area.intro_text,
        }


class ArticleAuthor(Orderable, models.Model):
    page = ParentalKey('Article', on_delete=models.CASCADE,
                       related_name='article_authors')
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name='+')

    panels = [
        SnippetChooserPanel('person'),
    ]


class Article(ListableMixin, StopwatchPage):
    template = 'stopwatch/pages/article.html'

    tags = ClusterTaggableManager(through=ArticleTag, blank=True)

    import_ref = models.IntegerField(null=True, blank=True)

    summary = StreamField(TEXT_MODULES, min_num=0, blank=True)
    body = StreamField(CONTENT_MODULES, min_num=0, blank=True)

    @property
    def hide_related_articles(self):
        category = self.category
        if category:
            return self.category.hide_related_articles

        else:
            return True

    @property
    def hide_date(self):
        category = self.category
        if category:
            return self.category.hide_dates

        else:
            return True

    search_fields = Page.search_fields + [
        index.FilterField('tag_id')
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('photo'),
        StreamFieldPanel('summary'),
        StreamFieldPanel('body'),
        FieldPanel('first_published_at'),

        MultiFieldPanel([
            InlinePanel('article_authors'),
        ], 'Authors'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]

    @property
    def authors(self):
        return [
            x.person
            for x
            in self.article_authors.all()
        ]

    @property
    def author_names(self):
        authors = self.authors
        if len(authors) == 0:
            return None

        if len(authors) == 1:
            return authors[0].name

        first = authors[:-1]
        last = authors[-1]

        return ', '.join(x.name for x in first) + ' & ' + last.name

    @property
    def related_articles(self):
        # TODO: Use tags to determine this once we have tags.
        return list(get_children_of_type(self.get_parent(), Article).exclude(pk=self.id)[:5])


class Form(ListableMixin, StopwatchPage, AbstractEmailForm):
    template = 'stopwatch/pages/form.html'
    landing_page_template = 'stopwatch/pages/form_submitted.html'
    intro = RichTextField(blank=True)
    thank_you_page = StreamField(CONTENT_MODULES)

    class FormField(AbstractFormField):
        page = ParentalKey('Form', on_delete=models.CASCADE,
                           related_name='form_fields')

    @property
    def description(self):
        return self.intro

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('photo'),
        InlinePanel('form_fields', label="Form fields"),
        StreamFieldPanel('thank_you_page', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]


class Category(ListableMixin, ChildListMixin, StopwatchPage):
    allow_search = True
    template = 'stopwatch/pages/category.html'

    description = models.TextField(null=True, blank=True)
    searchable = models.BooleanField(default=False)
    newsflash = models.BooleanField(default=False)
    navigable = models.BooleanField(default=True)
    style = models.CharField(
        max_length=128,
        choices=ArticlesListBlock.StyleChoices.options,
        default=ArticlesListBlock.StyleChoices.GRID)

    hide_related_articles = models.BooleanField(default=True)
    hide_dates = models.BooleanField(default=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('photo'),
        FieldPanel('style'),
        FieldPanel('searchable'),
        FieldPanel('newsflash'),
        FieldPanel('navigable'),
    ]

    @classmethod
    def get_display_options(cls):
        return super().get_display_options() + [
            FieldPanel('hide_related_articles'),
            FieldPanel('hide_dates'),
        ]

    def serve(self, request, *args, **kwargs):
        if not self.navigable:
            return HttpResponseNotFound()

        return super().serve(request, *args, **kwargs)

    @property
    def is_routable(self):
        return self.navigable

    def get_page_size(self):
        return 25

    @django_cached('stopwatch.models.Category.tags', lambda category: category.get_parent().id)
    def tags(self):
        '''
        Return all tags that apply to articles in this category
        '''

        all_tags = set()
        for article in get_children_of_type(self, Article).iterator():
            for tag in article.tags.all():
                all_tags.add(tag.id)

        return list(Tag.objects.filter(id__in=all_tags))

    def get_filters(self, request):
        tag = request.GET.get('theme', None)
        if tag is not None:
            try:
                return {
                    'tags': Tag.objects.get(slug=tag)
                }
            except Tag.DoesNotExist:
                pass

    def get_filter_form(self, request):
        from stopwatch.forms import CategoryFilterForm
        return CategoryFilterForm(data=request.GET, tags=self.tags())

    def get_child_list_queryset(self, request):
        filters = self.get_filters(request)

        if filters and 'tags' in filters:
            # Only articles can be filtered by tag
            return get_children_of_type(self, Article)
        else:
            return self.get_children().live().specific()

    @property
    def featured_items(self):
        return self.get_children().live().order_by('-first_published_at').specific()[:10]


class ExternalPage(ListableMixin, StopwatchPage):
    target_url = URLField()
    description = RichTextField(blank=True, null=True)
    photo = models.ForeignKey(
        StopwatchImage, null=True, blank=True, on_delete=models.SET_NULL)

    content_panels = Page.content_panels + [
        FieldPanel('target_url'),
    ]

    def serve(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.target_url)
