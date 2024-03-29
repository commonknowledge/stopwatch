from stopwatch.models.pages import StopwatchPage
from django.http.response import HttpResponseRedirect
from stopwatch.models.mixins import ListableMixin
from django.db.models.fields.related import ForeignKey
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from wagtail.core.models import Orderable, Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, FieldPanel, FieldPanel, PageChooserPanel, InlinePanel
from wagtail.snippets.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from django.db import models
from colorfield.fields import ColorField
from wagtail.images.edit_handlers import FieldPanel
from stopwatch.models import CONTENT_MODULES
from commonknowledge.wagtail.models import ChildListMixin, SortOption
from commonknowledge.wagtail.helpers import get_children_of_type
from colour import Color


class Project(ListableMixin, StopwatchPage):
    template = 'projects/pages/project.html'
    parent_page_types = ('stopwatch.Category',)

    photo = models.ForeignKey(
        'stopwatch.StopwatchImage', null=True, blank=True, on_delete=models.SET_NULL)

    description = RichTextField()
    color = ColorField()
    body = StreamField(CONTENT_MODULES)

    content_panels = Page.content_panels + [
        FieldPanel('photo'),
        FieldPanel('description'),
        FieldPanel('color'),
        FieldPanel('body'),
    ]

    @property
    def pages(self):
        return self.get_children().filter(show_in_menus=True)

    @property
    def themes(self):
        return get_children_of_type(self.project, EventTheme)

    @property
    def project(self):
        return self

    @property
    def contrast_color(self):
        col = Color(self.color)
        if col.luminance < 0.5:
            return '#FFF'
        else:
            return '#000'


class ProjectPage(StopwatchPage):
    class Meta:
        abstract = True

    @cached_property
    def project(self) -> Project:
        parent = self.get_parent().specific
        if isinstance(parent, Project):
            return parent

        return parent.project


class ProjectArticle(ListableMixin, ProjectPage):
    template = 'projects/pages/article.html'

    parent_page_types = (Project,)
    photo = models.ForeignKey(
        'stopwatch.StopwatchImage', null=True, blank=True, on_delete=models.SET_NULL)

    description = RichTextField()


class ProjectEvents(ChildListMixin, ProjectPage):
    template = 'projects/pages/project_events.html'
    parent_page_types = (Project,)

    def get_filters(self, request):
        theme = request.GET.get('theme', None)
        if theme:
            return {
                'theme__slug': theme
            }

    def get_sort(self, request):
        return SortOption('Newest', 'newest', 'start_time')

    def get_child_list_queryset(self, request):
        return get_children_of_type(self, Event)

    @property
    def themes(self):
        return self.project.themes

    def get_filter_form(self, request):
        from projects.forms import EventFilterForm
        return EventFilterForm(data=request.GET, themes=self.themes)


class EventTheme(ListableMixin, ProjectPage):
    parent_page_types = (Project,)
    photo = models.ForeignKey(
        'stopwatch.StopwatchImage', null=True, blank=True, on_delete=models.SET_NULL)
    color = ColorField()
    background_color = ColorField()
    description = models.TextField()
    body = StreamField(CONTENT_MODULES)

    content_panels = Page.content_panels + [
        FieldPanel('photo'),
        FieldPanel('description'),
        FieldPanel('color'),
        FieldPanel('background_color'),
        FieldPanel('body'),
    ]

    def serve(self, request, *args, **kwargs):
        events_page = get_children_of_type(self.project, ProjectEvents).first()

        if events_page is None:
            return HttpResponseRedirect(self.project.url)

        return HttpResponseRedirect(f'{events_page.url}?theme={self.slug}')


class EventSpeaker(Orderable, models.Model):
    page = ParentalKey('Event', on_delete=models.CASCADE,
                       related_name='event_speakers')
    person = models.ForeignKey(
        'stopwatch.Person', on_delete=models.CASCADE, related_name='+')

    panels = [
        FieldPanel('person'),
    ]


class Event(ListableMixin, ProjectPage):
    template = 'projects/pages/event.html'
    parent_page_types = (ProjectEvents,)

    photo = models.ForeignKey(
        'stopwatch.StopwatchImage', null=True, blank=True, on_delete=models.SET_NULL)

    summary = RichTextField(max_length=1024, default='', blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    theme = models.ForeignKey(
        EventTheme, on_delete=models.SET_NULL, null=True, blank=True)

    registration_page = models.URLField(
        blank=True, null=True, verbose_name='Registration link')
    body = StreamField(CONTENT_MODULES, verbose_name='Event details')

    @property
    def speakers(self):
        return tuple(
            speaker.person
            for speaker
            in self.event_speakers.all()
        )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('photo'),
            PageChooserPanel('theme'),
            FieldPanel('registration_page'),
            FieldPanel('summary'),
        ], 'Basics'),

        MultiFieldPanel([
            FieldPanel('start_time'),
            FieldPanel('end_time'),
        ], 'Timings'),

        MultiFieldPanel([
            InlinePanel('event_speakers'),
        ], 'Speakers'),

        FieldPanel('body'),
    ]
