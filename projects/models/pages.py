from django.db.models.fields.related import ForeignKey
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from wagtail.core.models import Orderable, Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, RichTextFieldPanel, StreamFieldPanel, PageChooserPanel, InlinePanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from django.db import models
from colorfield.fields import ColorField
from wagtail.images.edit_handlers import ImageChooserPanel
from stopwatch.models import CONTENT_MODULES
from commonknowledge.wagtail.models import ChildListMixin
from commonknowledge.wagtail.helpers import get_children_of_type


class Project(Page):
    template = 'projects/pages/project.html'

    photo = models.ForeignKey(
        'stopwatch.StopwatchImage', null=True, blank=True, on_delete=models.SET_NULL)

    description = RichTextField()
    color = ColorField()
    body = StreamField(CONTENT_MODULES)

    content_panels = Page.content_panels + [
        ImageChooserPanel('photo'),
        RichTextFieldPanel('description'),
        FieldPanel('color'),
        StreamFieldPanel('body'),
    ]

    @property
    def project(self):
        return self


class ProjectPage(Page):
    class Meta:
        abstract = True

    @cached_property
    def project(self) -> Project:
        parent = self.get_parent().specific
        if isinstance(parent, Project):
            return parent

        return parent.project


class ProjectArticle(ProjectPage):
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
        if theme is not None:
            return {
                'theme__slug': theme
            }

    def get_child_list_queryset(self):
        return get_children_of_type(self, Event)

    @property
    def themes(self):
        return get_children_of_type(self.project, EventTheme).specific()


class EventTheme(ProjectPage):
    template = 'projects/pages/theme.html'

    parent_page_types = (Project,)
    photo = models.ForeignKey(
        'stopwatch.StopwatchImage', null=True, blank=True, on_delete=models.SET_NULL)
    color = ColorField()
    description = models.TextField()
    body = StreamField(CONTENT_MODULES)

    content_panels = Page.content_panels + [
        ImageChooserPanel('photo'),
        RichTextFieldPanel('description'),
        FieldPanel('color'),
        StreamFieldPanel('body'),
    ]


class EventSpeaker(Orderable, models.Model):
    page = ParentalKey('Event', on_delete=models.CASCADE,
                       related_name='event_speakers')
    person = models.ForeignKey(
        'stopwatch.Person', on_delete=models.CASCADE, related_name='+')

    panels = [
        SnippetChooserPanel('person'),
    ]


class Event(ProjectPage):
    template = 'projects/pages/event.html'
    parent_page_types = (ProjectEvents,)

    photo = models.ForeignKey(
        'stopwatch.StopwatchImage', null=True, blank=True, on_delete=models.SET_NULL)

    intro_text = RichTextField(max_length=1024, default='', blank=True)
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
            ImageChooserPanel('photo'),
            PageChooserPanel('theme'),
            RichTextFieldPanel('registration_page'),
            RichTextFieldPanel('intro_text'),
        ], 'Basics'),

        MultiFieldPanel([
            FieldPanel('start_time'),
            FieldPanel('end_time'),
        ], 'Timings'),

        MultiFieldPanel([
            InlinePanel('event_speakers'),
        ], 'Speakers'),

        StreamFieldPanel('body'),
    ]
