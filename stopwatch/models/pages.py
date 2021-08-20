from django.db.models.fields import URLField
from django.db.models.fields.related import RelatedField
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core.fields import RichTextField, StreamField
from django.http.response import HttpResponseRedirect
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from taggit.models import Tag, TaggedItemBase
from commonknowledge.wagtail.helpers import get_children_of_type
from commonknowledge.wagtail.models import ChildListMixin
from commonknowledge.django.cache import django_cached

from stopwatch.models.core import Person, SiteSettings, StopwatchImage
from stopwatch.models.components import CONTENT_MODULES, TEXT_MODULES, LANDING_MODULES


class ArticleTag(TaggedItemBase):
    content_object = ParentalKey(
        'Article', on_delete=models.CASCADE, related_name='tagged_items')


class LandingPage(Page):
    template = 'stopwatch/pages/landing.html'

    page_description = models.CharField(max_length=512, default='')
    landing_video = models.URLField(blank=True, null=True)

    body = StreamField(LANDING_MODULES, min_num=0, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('page_description'),
        FieldPanel('landing_video'),
        StreamFieldPanel('body'),
    ]


class ArticleAuthor(Orderable, models.Model):
    page = ParentalKey('Article', on_delete=models.CASCADE,
                       related_name='article_authors')
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name='+')

    panels = [
        SnippetChooserPanel('person'),
    ]


class Article(Page):
    template = 'stopwatch/pages/article.html'

    tags = ClusterTaggableManager(through=ArticleTag, blank=True)

    import_ref = models.IntegerField(null=True, blank=True)
    photo = models.ForeignKey(
        StopwatchImage, null=True, blank=True, on_delete=models.SET_NULL)

    intro_text = models.CharField(max_length=1024, default='', blank=True)
    summary = StreamField(TEXT_MODULES, min_num=0, blank=True)
    body = StreamField(CONTENT_MODULES, min_num=0, blank=True)

    search_fields = Page.search_fields + [
        index.FilterField('tag_id')
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('photo'),
        FieldPanel('intro_text'),
        StreamFieldPanel('summary'),
        StreamFieldPanel('body'),

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
        return list(get_children_of_type(self.get_parent(), Article)[:5])


class Form(AbstractEmailForm):
    template = 'stopwatch/pages/form.html'
    landing_page_template = 'stopwatch/pages/form_submitted.html'

    intro = RichTextField(blank=True)
    thank_you_page = StreamField(CONTENT_MODULES)

    class FormField(AbstractFormField):
        page = ParentalKey('Form', on_delete=models.CASCADE,
                           related_name='form_fields')

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
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


class Category(ChildListMixin, Page):
    allow_search = True
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

    @django_cached('stopwatch.models.Category.tags', lambda category: category.get_parent().id)
    def tags(self):
        '''
        Return all tags that apply to articles in this category
        '''

        all_tags = set()
        for article in self.get_child_list_queryset().iterator():
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

    def get_child_list_queryset(self):
        return get_children_of_type(self, Article).order_by('-first_published_at')

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
